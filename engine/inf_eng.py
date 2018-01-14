from defuzzy.defuzzifier import Defuzzifier
from engine.sem_err import InferenceEngineException
from fuzzy.i_fuzzy import FuzzySet
from fuzzy.i_unary import UnaryFunction
from fuzzy.sets.calculated import CalculatedFuzzySet
from parser.elements.element_conj import ElementConjunction, Conjunction
from parser.nodes.antecedent_node import AntecedentNode
from parser.nodes.consequent_node import ConsequentNode
from parser.nodes.if_then_node import IfThenNode
from parser.nodes.parameter_node import ParameterNode
from parser.nodes.variable_node import VariableNode
from property.param import ParameterProperty


class InferenceEngine:
    def __init__(self, rules: dict, properties: dict, target_value: str, implication, s_norm,
                 t_norm, complement: UnaryFunction, defuzzifier: Defuzzifier, multi_output: bool = False,
                 is_composition: bool = False, is_global_semantic: bool = False):
        self.multi_output = multi_output
        self.implication = implication
        self.s_norm = s_norm
        self.t_norm = t_norm
        self.complement = complement
        self.is_composition = is_composition
        self.is_global_semantic = is_global_semantic
        self.target_value = target_value
        self.defuzzifier = defuzzifier
        self.rule_sets = self.process_base(rules[target_value], properties)

    # @staticmethod
    # def load_rules_from_file(file):
    #     lines = (line.rstrip('\n') for line in open(file))
    #     rules = '\n'.join(lines)
    #     rule_parser = RuleParser(rules)
    #     return rule_parser.get_document_node()
    #
    # @staticmethod
    # def load_properties(file):
    #     pr = PropertiesReader(file + '/modifier', file + '/params')
    #     return pr.get_parameters()

    def process_base(self, rules: list, par_properties: dict):
        rule_sets = []
        for rule in rules:
            if not isinstance(rule, IfThenNode):
                raise InferenceEngineException("Rules should be made of If-Then expressions: ", str(rule))
            rule_sets.append(self.process_rule(rule, par_properties))

        return rule_sets

    def process_rule(self, rule: IfThenNode, par_properties: dict) -> (object, FuzzySet):
        if len(rule.children) < 0 and not isinstance(rule.get_child(0), AntecedentNode) and \
                not isinstance(rule.get_child(1), ConsequentNode):
            raise InferenceEngineException("If-Then expressions should be made of Antecedent and Consequent:", str(rule))
        antecedent = self.process_antecedent(rule.get_child(0), par_properties)
        consequent = self.process_consequent(rule.get_child(1), par_properties)
        # implied = consequent.imply(self.implication, antecedent(*x_s))
        return antecedent, consequent
        # return lambda x_s, y_s: self.implication(antecedent(*x_s), consequent(*y_s))

    def process_antecedent(self, ant_node: AntecedentNode, par_properties: dict) -> object:
        return self.process_multi_output(ant_node, par_properties)

    def process_consequent(self, cons_node: ConsequentNode, par_properties: dict) -> CalculatedFuzzySet:
        if not self.multi_output:
            if len(cons_node.children) > 1:
                raise InferenceEngineException("Expected only one parameter definition: ", str(cons_node))
            param_node = cons_node.get_child(0)
            self.check_if_param(param_node)
            if str(param_node.param) != self.target_value:
                raise InferenceEngineException("Expected", self.target_value, "got", str(param_node.param))
            parameter_property = par_properties[str(param_node.param)]
            return CalculatedFuzzySet(parameter_property.get_domain(),
                                      self.process_parameter_node(param_node, parameter_property))
        else:
            raise NotImplementedError  # TODO - implementirati MIMO
            # return self.process_multi_output(cons_node, par_properties)

    def process_multi_output(self, node, par_properties: dict) -> object:
        if len(node.children) < 1:
            raise InferenceEngineException("Expected at least one parameter definition", str(node))
        param_sets = []
        # first param
        param_node = node.get_child(0)
        self.check_if_param(param_node)
        parameter_property = par_properties[str(param_node.param)]
        param_sets.append((parameter_property.get_param_name(), CalculatedFuzzySet(parameter_property.get_domain(),
                                                                                   self.process_parameter_node(
                                                                                       param_node,
                                                                                       parameter_property))))
        for i in range(node.number_of_children() - 1):
            param_node = node.get_child(i + 1)
            self.check_if_param(param_node)
            parameter_property = par_properties[str(param_node.param)]
            param_sets.append((parameter_property.get_param_name(), CalculatedFuzzySet(parameter_property.get_domain(),
                                                                                       self.process_parameter_node(
                                                                                           param_node,
                                                                                           parameter_property))))
        return self.big_t_norm(param_sets)

    def process_parameter_node(self, param_node: ParameterNode, parameter_property: ParameterProperty) -> object:
        var_node = param_node.get_child(0)
        self.check_if_var(var_node)
        membership_fun = self.process_variable_node(var_node, parameter_property)
        for i in range(param_node.number_of_children() - 1):
            var_node = param_node.get_child(i + 1)
            self.check_if_var(var_node)
            membership_fun = self.perf_norm(param_node.conjunctions[i], membership_fun,
                                            self.process_variable_node(var_node, parameter_property))

        if not param_node.is_t.is_flag:
            return lambda x: self.complement(membership_fun(x))

        return membership_fun
    @staticmethod
    def check_if_param(param_node):
        if not isinstance(param_node, ParameterNode):
            raise InferenceEngineException("Expected Parameter expressions: ", str(param_node))

    @staticmethod
    def check_if_var(var_node):
        if not isinstance(var_node, VariableNode):
            raise InferenceEngineException("Expected Variable expressions: ", str(var_node))

    def perf_norm(self, conjunction: ElementConjunction, f1: UnaryFunction or object,
                  f2: UnaryFunction or object) -> object:
        if conjunction.conj == Conjunction.ILI:
            return lambda x: self.s_norm(f1(x), f2(x))
        else:
            return lambda x: self.t_norm(f1(x), f2(x))

    def big_t_norm(self, param_sets: list) -> object:
        this = self

        def tt(x: dict):
            return this.t_norm(*[param_sets[i][1](x[param_sets[i][0]]) for i in range(len(param_sets))])

        return tt

    @staticmethod
    def process_variable_node(var_node: VariableNode, parameter_property: ParameterProperty) -> UnaryFunction:
        if len(var_node.children) > 0:
            raise InferenceEngineException("Variable node should not contain nested expressions: ", str(var_node))
        membership_fun = parameter_property.get_variable_by_name(str(var_node.variable)).get_function()
        for mod in var_node.modifiers:
            membership_fun = parameter_property.get_modifier_by_name(str(mod)).wrap_function(membership_fun)
        return membership_fun

    def infer(self, x_s: dict) -> FuzzySet:

        infer_fun = self.t_norm if self.is_global_semantic else self.s_norm
        if self.is_composition:
            # TODO - prvo stvoriti jednu veliku lambda funkciju i onda tek predati x_s i y_s
            raise NotImplementedError
        else:
            antecedent, consequent = self.rule_sets[0]
            inferred_set = consequent.imply(self.implication, antecedent(x_s))
            for i in range(1, len(self.rule_sets)):
                antecedent, consequent = self.rule_sets[i]
                implied_set = consequent.imply(self.implication, antecedent(x_s))
                inferred_set = inferred_set.perform_binary(implied_set, infer_fun)

            return self.defuzzifier.defuzzify(inferred_set)

from parser.elements.element_conj import ElementConjunction
from parser.elements.element_is import ElementIsNot
from parser.elements.element_mod import ElementModifier
from parser.elements.element_param import ElementParameter
from parser.elements.element_var import ElementVariable
from parser.lexer.lexer_err import LexerException
from parser.lexer.rule_lexer import Lexer
from parser.lexer.token_type import TokenType
from parser.nodes.antecedent_node import AntecedentNode
from parser.nodes.consequent_node import ConsequentNode
from parser.nodes.document_node import DocumentNode
from parser.nodes.if_then_node import IfThenNode
from parser.nodes.parameter_node import ParameterNode
from parser.nodes.variable_node import VariableNode
from parser.parser_err import ParserException


class RuleParser:
    def __init__(self, text):
        self.main_node = self.parse(Lexer(text))

    def parse(self, lexer):
        main_node = DocumentNode()
        token_list = []
        tokens = lexer.tokens()
        try:
            # First IF
            while True:
                token = next(tokens)
                if token.type != TokenType.COMMENT:
                    break
            if token.type != TokenType.IF:
                raise ParserException("Expected IF at the beginning of the rule!")
            if_then_node = IfThenNode()
            main_node.add_child_node(if_then_node)
            then_expect = True
            for token in tokens:
                if token.type == TokenType.IF:
                    if then_expect:
                        raise ParserException("Expected THEN before new IF!")
                    then_expect = True
                    if_then_node.add_child_node(self.handle_consequent(token_list))
                    if_then_node = IfThenNode()
                    main_node.add_child_node(if_then_node)
                elif token.type == TokenType.THEN:
                    if not then_expect:
                        raise ParserException("Expected IF before THEN!")
                    then_expect = False
                    if_then_node.add_child_node(self.handle_antecedent(token_list))
                elif token.type == TokenType.COMMENT:
                    pass
                else:
                    token_list.append(token)
            # finally
            if_then_node.add_child_node(self.handle_consequent(token_list))
        except LexerException as exc:
            raise ParserException('Lexer error') from exc

        return main_node

    # def add_to_stack(self, child):
    #     self.node_stack[TOP].add_child_node(child)
    #
    # def stack_and_add(self, child):
    #     self.node_stack.append(child)
    #     self.node_stack[PREVIOUS].add_child_node(self.node_stack[TOP])

    def get_document_node(self):
        return self.main_node

    def handle_if_then(self, token_list):
        expect_conjunction = False
        in_quotation = False
        conjunctions = []
        predicates = []
        index_first = -1
        index_last = -1
        for token in token_list:
            if token.type == TokenType.PARAM:
                if expect_conjunction:
                    raise ParserException('Conjunction AND' +
                                          ' was expected before another predicate! Antecedent = '
                                          + self.str_token_list(token_list))
                expect_conjunction = True
                if index_last > index_first:
                    predicates.append(self.handle_predicate(token_list[index_first:index_last]))
                index_last += 2
                index_first = index_last - 1
            elif token.type == TokenType.AND and (not in_quotation):
                if not expect_conjunction:
                    raise ParserException('Missing predicate in between two conjunctions! Antecedent = '
                                          + self.str_token_list(token_list))
                expect_conjunction = False
                conjunctions.append(ElementConjunction(token.value))
            elif token.type == TokenType.QUOTE:
                in_quotation = not in_quotation
                index_last += 1
            else:
                index_last += 1
        if not expect_conjunction:
            raise ParserException('Another predicate was expected after last conjunction! Antecedent = '
                                  + self.str_token_list(token_list))
        predicates.append(self.handle_predicate(token_list[index_first:index_last]))
        token_list.clear()
        return predicates, conjunctions

    def handle_antecedent(self, token_list):
        predicates, conjunctions = self.handle_if_then(token_list)
        antecedent = AntecedentNode(conjunctions)
        for predicate in predicates:
            antecedent.add_child_node(predicate)

        return antecedent

    def handle_predicate(self, token_list):
        if len(token_list) < 5:
            raise ParserException('Predicate must have a least five characters = [<param>, is, \", '
                                  '<variable>, \"]! Predicate = ' + self.str_token_list(token_list))
        param = token_list[0]
        is_t = token_list[1]
        q_first = token_list[2]
        variables = token_list[3:-1]
        q_last = token_list[-1]

        if param.type != TokenType.PARAM or (is_t.type != TokenType.IS and is_t.type != TokenType.NOT) \
                or q_first.type != TokenType.QUOTE or q_last.type != TokenType.QUOTE or \
                any(t.type not in (TokenType.WORD, TokenType.AND, TokenType.OR) for t in variables):
            raise ParserException('Predicate is not in correct form : <param> is \" <words> \"! Predicate = '
                                  + self.str_token_list(token_list))

        variable_exps, conjunctions = self.handle_complex_exp(variables)
        param_node = ParameterNode(ElementParameter(param.value), ElementIsNot(is_t.value), conjunctions)
        for exp in variable_exps:
            param_node.add_child_node(exp)

        return param_node

    def handle_complex_exp(self, token_list):
        expect_word = True
        conjunctions = []
        variable_exps = []
        index_first = 0
        index_last = 0
        for token in token_list:
            if token.type == TokenType.WORD:
                expect_word = False
                index_last += 1
            elif token.type == TokenType.OR or token.type == TokenType.AND:
                if expect_word:
                    raise ParserException('Expected a variable before conjunction:' + str(token.value) +
                                          '! Complex expression = '
                                          + self.str_token_list(token_list))
                expect_word = True
                conjunctions.append(ElementConjunction(token.value))
                variable_exps.append(self.handle_simple_exp(token_list[index_first:index_last]))
                index_last += 1
                index_first = index_last
            else:
                raise ParserException('Expected a <modifier>, <variable> or <conjunction>!' +
                                      '! Complex expression = '
                                      + self.str_token_list(token_list))
        if expect_word:
            raise ParserException('Another variable was expected after last conjunction! Complex expression = '

                                  + self.str_token_list(token_list))
        variable_exps.append(self.handle_simple_exp(token_list[index_first:index_last]))

        return variable_exps, conjunctions

    @staticmethod
    def handle_simple_exp(token_list):
        return VariableNode(modifiers=[ElementModifier(mod.value) for mod in token_list[0:-1]],
                            variable=ElementVariable(token_list[-1].value))

    def handle_consequent(self, token_list):
        predicates, conjunctions = self.handle_if_then(token_list)
        consequent = ConsequentNode(conjunctions)
        for predicate in predicates:
            consequent.add_child_node(predicate)

        return consequent

    @staticmethod
    def str_token_list(token_list):
        return ' '.join([str(token.value) for token in token_list])

    def print_parse_tree(self):
        current_node = self.main_node
        print(str(current_node))
        RuleParser.print_recursion(current_node, 1)

    @staticmethod
    def print_recursion(node, level):
        for child in node.children:
            print(("-" * level), str(child))
            RuleParser.print_recursion(child, level + 1)


if __name__ == "__main__":
    rule = "AKO L je \"Kritično blizu ILI Blizu I daleko\" I LK je \"Kritično daleko\" I NK je \"dinamo\" ONDA K je \"Oštro desno\"\n #fefefefefe\n " \
           "AKO L " \
           "nije \"blizu\" ONDA K je \"lijevo\""
    rp = RuleParser(rule)
    rp.print_parse_tree()

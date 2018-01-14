from parser.elements.element_is import ElementIsNot
from parser.nodes.abs_conj_node import AbstractConjunctionNode


class ParameterNode(AbstractConjunctionNode):

    def __init__(self, param, is_t: ElementIsNot, conjunctions: "list of ElementConjunctions"):
        super().__init__(conjunctions)
        self.param = param
        self.is_t = is_t

    def __repr__(self):
        return "ParameterNode(param = " + str(self.param) + ", is_t = " + str(self.is_t) + ", " + super().__repr__()

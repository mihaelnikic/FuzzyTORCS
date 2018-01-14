from parser.nodes.abs_conj_node import AbstractConjunctionNode


class AntecedentNode(AbstractConjunctionNode):

    def __repr__(self):
        return "AntecedentNode(" + super().__repr__()

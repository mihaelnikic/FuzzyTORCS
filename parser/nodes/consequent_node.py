from parser.nodes.abs_conj_node import AbstractConjunctionNode


class ConsequentNode(AbstractConjunctionNode):

    def __repr__(self):
        return "ConsequentNode(" + super().__repr__()

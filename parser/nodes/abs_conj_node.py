from parser.nodes.node import Node
import abc


class AbstractConjunctionNode(Node):
    __metaclass__ = abc.ABCMeta

    def __init__(self, conjunctions: list):
        super().__init__()
        self.conjunctions = conjunctions

    def __repr__(self):
        return "conjunctions = " + str([str(conj) for conj in self.conjunctions]) + ")"

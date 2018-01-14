from parser.elements.element_var import ElementVariable
from parser.nodes.node import Node


class VariableNode(Node):
    def __init__(self, modifiers: list, variable: ElementVariable):
        super().__init__()
        self.modifiers = modifiers
        self.variable = variable

    def __repr__(self):
        return "VariableNode(modifiers = " + str([str(mod) for mod in self.modifiers]) + ", variable = " \
               + str(self.variable) + ")"

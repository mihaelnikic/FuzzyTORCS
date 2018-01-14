from enum import Enum

from fuzzy.i_unary import UnaryFunction
from fuzzy.modifiers.contraction import ContractionModifier
from fuzzy.modifiers.contrast_int import ContrastIntensificationModifier
from fuzzy.modifiers.dilatation import DilatationModifier
from fuzzy.modifiers.less import LessModifier
from fuzzy.modifiers.more import MoreModifier


class ModifierPropertyFunctions(Enum):
    CONTRACTION = ContractionModifier
    DILATATION = DilatationModifier
    MORE = MoreModifier
    LESS = LessModifier
    CONTRAST_INT = ContrastIntensificationModifier


class ModifierProperty:
    def __init__(self, name: str, func: str):
        self.name = name
        self.func = ModifierPropertyFunctions[func].value

    def get_modifier_name(self):
        return self.name

    def wrap_function(self, target_function: UnaryFunction) -> UnaryFunction:
        return self.func(target_function)

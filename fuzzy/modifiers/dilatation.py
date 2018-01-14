from fuzzy.modifiers.i_modifier import AbstractModifier
import math


class DilatationModifier(AbstractModifier):
    def abstract_get_value(self, x):
        return math.sqrt(x)
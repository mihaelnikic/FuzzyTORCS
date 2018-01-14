from fuzzy.modifiers.i_modifier import AbstractModifier


class NegationModifier(AbstractModifier):
    def abstract_get_value(self, x):
        return 1 - x
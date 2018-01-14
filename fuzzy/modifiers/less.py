from fuzzy.modifiers.i_modifier import AbstractModifier


class LessModifier(AbstractModifier):
    def abstract_get_value(self, x):
        return x**0.75
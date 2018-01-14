from fuzzy.modifiers.i_modifier import AbstractModifier


class ContractionModifier(AbstractModifier):
    def abstract_get_value(self, x):
        return x**2
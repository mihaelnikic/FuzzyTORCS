from fuzzy.modifiers.i_modifier import AbstractModifier


class MoreModifier(AbstractModifier):
    def abstract_get_value(self, x):
        return x**1.25
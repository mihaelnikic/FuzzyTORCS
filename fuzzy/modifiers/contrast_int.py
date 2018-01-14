from fuzzy.modifiers.i_modifier import AbstractModifier


class ContrastIntensificationModifier(AbstractModifier):
    def abstract_get_value(self, x):
        if x <= 0.5:
            return 2 * (x ** 2)
        else:
            return 1 - 2 * ((1 - x) ** 2)
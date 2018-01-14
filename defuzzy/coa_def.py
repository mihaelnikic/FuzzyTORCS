from defuzzy.defuzzifier import Defuzzifier
from fuzzy.i_fuzzy import FuzzySet
from fuzzy.utils import debug


class COADefuzzifier(Defuzzifier):
    def __init__(self, debug=False):
        self.debug = debug

    def defuzzify(self, inferred_set: FuzzySet) -> float:
        if self.debug:
            debug.s_print(inferred_set, "Zaključak: ")
        numerator, denominator = 0, 0
        for elem in inferred_set.get_domain():
            value_at_elem = inferred_set.get_value_at(elem)
            numerator += elem * value_at_elem
            denominator += value_at_elem
        if denominator == 0:
            return 0
        return round(numerator / denominator)

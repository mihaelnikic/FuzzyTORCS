import numpy as np
from fuzzy.sets.calculated import CalculatedFuzzySet

from defuzzy.defuzzifier import Defuzzifier
from fuzzy.domain.simple_domain import SimpleDomain
from fuzzy.i_fuzzy import FuzzySet
from fuzzy.utils import debug


class COGDefuzzifier(Defuzzifier):
    def __init__(self, debug=False):
        self.debug = debug

    def defuzzify(self, inferred_set: FuzzySet) -> float:
        if self.debug:
            debug.s_print(inferred_set, "Zaključak: ")
        domain = inferred_set.get_domain()
        domain_elems = np.linspace(domain.first, domain.last, num=100)
        approximated_set = np.array([inferred_set.get_value_at(elem) for elem in domain_elems])
        numerator = np.trapz(approximated_set * np.array(domain_elems), domain_elems)
        denominator = np.trapz(approximated_set, domain_elems)
        if denominator == 0:
            return 0
        return numerator / denominator

if __name__ == "__main__":
    defuzz = COGDefuzzifier()
    muset = CalculatedFuzzySet(SimpleDomain(0, 1), lambda x : x ** 2)
    print(defuzz.defuzzify(muset))
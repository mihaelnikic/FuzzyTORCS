from collections import defaultdict

from fuzzy.domain.i_domain import Domain
from fuzzy.i_fuzzy import FuzzySet


class MutableFuzzySet(FuzzySet):
    def __init__(self, domain: Domain):
        super().__init__(domain)
        self.func_values = defaultdict(float)

    def get_value_at(self, elem):
        return self.func_values[elem]

    def set(self, elem, value):
        #index = self.domain.index_of_element(elem)
        #if index is not None:
        self.func_values[elem] = value # TODO: IZBACITI DOMENU SKROZ
       # else:
       #     raise ValueError('Element ' + str(elem) + ' is not a part of specified domain')
        return self
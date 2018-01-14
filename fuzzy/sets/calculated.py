from fuzzy.domain.i_domain import Domain
from fuzzy.i_fuzzy import FuzzySet
from fuzzy.i_unary import UnaryFunction


class CalculatedFuzzySet(FuzzySet):
    def __init__(self, domain: Domain, fun: UnaryFunction or function):
        super().__init__(domain)
        self.fun = fun

    def get_value_at(self, x):
      #  i_x = self.get_domain().index_of_element(x) # TODO: IZBACITI DOMENU
        return self.fun(x)

    def imply(self, implication, value):
        implied = CalculatedFuzzySet(self.get_domain(), lambda elem : implication(self.get_value_at(elem), value))
        #implied = MutableFuzzySet(self.get_domain())
        #for elem in self.get_domain():
        #    implied.set(elem, implication(self.get_value_at(elem), value)) # TODO: ovdje partial
        return implied

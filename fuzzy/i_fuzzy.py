import abc

from fuzzy.domain.i_domain import Domain
from fuzzy.i_binary import BinaryFunction
from fuzzy.i_unary import UnaryFunction


class FuzzySet:
    __metaclass__ = abc.ABCMeta

    def __init__(self, domain: Domain):
        self.domain = domain

    def get_domain(self):
        return self.domain

    def perform_unary(self, unary_func: UnaryFunction or function):
        this = self

        class UnarySet(FuzzySet):
            def __init__(self):
                super().__init__(this.get_domain())

            def get_value_at(self, x):
                return unary_func(this.get_value_at(x))

        return UnarySet()

    def perform_binary(self, other_set, binary_func: BinaryFunction or function):
        this = self
        if this.get_domain() != other_set.get_domain():
            raise ValueError('Given set has to have the same domain!')

        class BinarySet(FuzzySet):
            def __init__(self):
                super().__init__(this.domain)

            def get_value_at(self, x):
                return binary_func(this.get_value_at(x), other_set.get_value_at(x))
        return BinarySet()

    def combine_sets(self, other_set,  fun):
        this = self
        d1_len = self.get_domain().get_dim()
        d = Domain.combine(self.get_domain(), other_set.get_domain())

        class CombinedSet(FuzzySet):
            def __init__(self):
                super().__init__(d)

            def get_value_at(self, *x):
                if len(x) < d.get_dim():
                    raise ValueError("Function takes " + str(x) + " arguments")
                return fun(this.get_value_at(*x[0: d1_len]), other_set.get_value_at(*x[d1_len:]))

        return CombinedSet()

    @abc.abstractclassmethod
    def get_value_at(self, elem):
        raise NotImplementedError

    def __call__(self, elem):
        return self.get_value_at(elem)

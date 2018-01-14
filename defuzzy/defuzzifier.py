import abc

from fuzzy.i_fuzzy import FuzzySet


class Defuzzifier:
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def defuzzify(self, inferred_set: FuzzySet):
        raise NotImplementedError

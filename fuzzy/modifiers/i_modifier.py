import abc

from fuzzy.i_unary import UnaryFunction


class AbstractModifier(UnaryFunction):
    __metaclass__ = abc.ABCMeta

    def __init__(self, unary: UnaryFunction):
        self.wrapped = unary

    def get_value_at(self, x: int):
        return self.abstract_get_value(self.wrapped.get_value_at(x))

    @abc.abstractclassmethod
    def abstract_get_value(self, x):
        raise NotImplementedError

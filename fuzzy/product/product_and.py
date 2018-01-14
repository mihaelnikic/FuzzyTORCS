import operator
import functools


class ProductAnd:
    @staticmethod
    def get_value_at(*x):
        return functools.reduce(operator.mul, x, 1)

    def __call__(self, *x):
        return self.get_value_at(x)

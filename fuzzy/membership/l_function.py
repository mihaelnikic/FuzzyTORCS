from fuzzy.i_unary import UnaryFunction


class LFunction(UnaryFunction):
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        if self.beta <= self.alpha:
            raise ValueError('Value of beta must be greater than value of alpha!')

    def get_value_at(self, x: int):
        if x < self.alpha:
            return 1.0
        elif x >= self.beta:
            return 0.0
        else:
            return (self.beta - x) / (self.beta - self.alpha)

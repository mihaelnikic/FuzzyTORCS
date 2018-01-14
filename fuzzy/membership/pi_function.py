from fuzzy.i_unary import UnaryFunction


class PiFunction(UnaryFunction):
    def __init__(self, alpha, beta, gamma, delta):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        if self.beta < self.alpha or self.gamma < self.beta or self.delta < self.gamma:
            raise ValueError('Value of beta must be greater than value of alpha!')

    def get_value_at(self, x: int):
        if x < self.alpha or x >= self.delta:
            return 0.0
        elif self.alpha <= x < self.beta:
            return (x - self.alpha) / (self.beta - self.alpha)
        elif self.beta <= x < self.gamma:
            return 1.0
        else:  # self.gamma <= x < self.delta:
            return (self.delta - x) / (self.delta - self.gamma)

from fuzzy.i_unary import UnaryFunction


class LambdaFunction(UnaryFunction):
    def __init__(self, alpha, beta, gamma):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        if self.beta < self.alpha or self.gamma < self.beta:
            raise ValueError('Value of beta must be greater than value of alpha and'
                             + ' value of gamma must be greater than value of beta!')

    def get_value_at(self, x: int):
        if (x < self.alpha) or (x >= self.gamma):
            return 0.0
        elif (x >= self.alpha) and (x < self.beta):
            return (x - self.alpha) / (self.beta - self.alpha)
        else:
            return (self.gamma - x) / (self.gamma - self.beta)

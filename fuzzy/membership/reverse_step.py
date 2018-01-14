from fuzzy.i_unary import UnaryFunction


class ReverseStepFunction(UnaryFunction):
    def __init__(self, threshold):
        self.threshold = threshold

    def get_value_at(self, x: int):
        if x > self.threshold:
            return 0.0
        else:
            return 1.0

from fuzzy.i_unary import UnaryFunction


class ExactlyFunction(UnaryFunction):

    def __init__(self, num):
        self.num = num

    def get_value_at(self, x: int):
        if x == self.num:
            return 1.0
        else:
            return 0.0

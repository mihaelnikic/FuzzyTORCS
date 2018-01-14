from fuzzy.i_unary import UnaryFunction


class ZadehNot(UnaryFunction):

    def get_value_at(self, x):
        return 1 - x

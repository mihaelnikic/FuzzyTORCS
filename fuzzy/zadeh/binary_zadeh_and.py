from fuzzy.i_binary import BinaryFunction


class BinaryZadehAnd(BinaryFunction):
    def get_value_at(self, x, y):
        return min(x, y)

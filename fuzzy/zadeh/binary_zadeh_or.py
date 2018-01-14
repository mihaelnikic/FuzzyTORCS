from fuzzy.i_binary import BinaryFunction


class ZadehOr(BinaryFunction):
    def get_value_at(self, x, y):
        return max(x, y)

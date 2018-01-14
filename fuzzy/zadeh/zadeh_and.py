

class ZadehAnd:
    @staticmethod
    def get_value_at(*x):
        return min(*x)

    def __call__(self, *x):
        return self.get_value_at(x)

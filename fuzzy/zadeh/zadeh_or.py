

class ZadehOr:
    @staticmethod
    def get_value_at(*x):
        return max(*x)

    def __call__(self, *x):
        return self.get_value_at(x)

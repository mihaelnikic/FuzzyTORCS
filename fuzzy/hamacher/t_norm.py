from fuzzy.i_binary import BinaryFunction


class HamacherT(BinaryFunction):
    def __init__(self, nu):
        self.nu = nu

    def get_value_at(self, x, y):
        return (x*y) / (self.nu + (1 - self.nu)*(x + y - x*y))

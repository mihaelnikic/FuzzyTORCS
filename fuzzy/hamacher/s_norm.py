from fuzzy.i_binary import BinaryFunction


class HamacherS(BinaryFunction):
    def __init__(self, nu):
        self.nu = nu

    def get_value_at(self, x, y):
        return (x + y - (2 - self.nu)*x*y) / (1 - (1 - self.nu)*x*y)

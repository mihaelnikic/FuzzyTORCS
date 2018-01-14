import abc


class BinaryFunction:
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def get_value_at(self, x, y):
        pass

    def __call__(self, x, y):
        return self.get_value_at(x, y)


import abc


class UnaryFunction:
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def get_value_at(self, x):
        pass

    def __call__(self, x):
        return self.get_value_at(x)


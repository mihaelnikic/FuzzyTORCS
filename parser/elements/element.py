import abc


class Element:
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def __repr__(self):
        raise NotImplementedError

from itertools import product
from itertools import islice


class Domain:
    def __init__(self, first, last):
        self.first = self.__to_tuple(first)
        self.last = self.__to_tuple(last)
        self.dim = len(self.first)
        if self.dim != len(self.last):
            raise ValueError('Both elements must have the same dimension!')

    @staticmethod
    def int_range(first: int, last: int):
        return Domain(first, last - 1)

    @staticmethod
    def combine(domain1, domain2):
        return Domain(domain1.first + domain2.first, domain1.last + domain2.last)

    @staticmethod
    def __to_tuple(number):
        if isinstance(number, tuple):
            return number
        elif isinstance(number, int):
            return number,
        else:
            raise ValueError('An element must be a number!')

    def cardinality(self):
        card = 1
        for l in range(len(self.first)):
            card *= self.last[l] - self.first[l] + 1
        return card

    def __iter__(self):
        for elem in product(*[range(self.first[i], self.last[i] + 1) for i in range(len(self.first))]):
            yield self.get_value(elem)

    def __getitem__(self, index):
        if index < 0:
            index = self.cardinality() + index
        return next(islice(self, index, None))

    def __eq__(self, other):
        if self.cardinality() != other.cardinality():
            return False
        for t, o in zip(self, other):
            if t != o:
                return False
        return True

    @staticmethod
    def get_value(domain_elem: tuple):
        return domain_elem if len(domain_elem) > 1 else domain_elem[0]

    def index_of_element(self, element):
        for i_x, x in enumerate(self):
            if element == x:
                return i_x

    def get_dim(self):
        return self.dim

    def get_first(self):
        return self.first

    def get_last(self):
        return self.last
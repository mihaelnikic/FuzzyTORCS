
from fuzzy.domain.i_domain import Domain


class SimpleDomain(Domain):
    def __init__(self, first, last):
        super().__init__(first, last)
        self.first = self.first[0]
        self.last = self.last[0]

    @staticmethod
    def combine(domain1, domain2):
        raise NotImplementedError

    def cardinality(self):
        return self.last - self.first + 1

    def __iter__(self):
        for i in range(self.first, self.last + 1):
            yield i

    def __getitem__(self, index):
        #assert index < 2
        if index < 0:
            index = self.cardinality() + index
        return self.first + index

    @staticmethod
    def get_value(domain_elem: tuple):
        raise ValueError()

    def index_of_element(self, element):
        return element #- self.first # TODO: IZBACITI DOMENU U POTPUNOSTI

    def get_dim(self):
        return self.dim

    def get_first(self):
        return self.first

    def get_last(self):
        return self.last

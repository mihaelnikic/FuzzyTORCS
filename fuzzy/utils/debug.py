from fuzzy.domain.i_domain import Domain
from fuzzy.i_fuzzy import FuzzySet


def d_print(domain: Domain, heading_text: str):
    if heading_text is not None:
        print(heading_text)
    for e in domain:
        print("Element domene:", e)
    print("Kardinalitet domene je:", domain.cardinality(), "\n")


def s_print(f_set: FuzzySet, heading_text: str):
    if heading_text is not None:
        print(heading_text)
    for d in f_set.get_domain():
        if isinstance(d, tuple):
            print('d(', d, ')=', f_set.get_value_at(*d))
        else:
            print('d(', d, ')=', f_set.get_value_at(d))
    print()

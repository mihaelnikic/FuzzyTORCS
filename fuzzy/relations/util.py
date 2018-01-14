from fuzzy.domain.i_domain import Domain
from fuzzy.i_fuzzy import FuzzySet
from fuzzy.sets.mutable import MutableFuzzySet

UxU_CARD = 2
MAX_ELEM_VALUE = 1
FIRST_DIM = 0
SECOND_DIM = 1


def is_u_times_u_relation(relation: FuzzySet):
    return relation.get_domain().get_dim() == UxU_CARD


def is_symmetric(relation: FuzzySet):
    if not is_u_times_u_relation(relation):
        return False
    for (x, y) in relation.get_domain():
        if relation.get_value_at((x, y)) != relation.get_value_at((y, x)):
            return False
    return True


def is_reflexive(relation: FuzzySet):
    if not is_u_times_u_relation(relation):
        return False
    for (x, y) in relation.get_domain():
        if x == y and relation.get_value_at((x, y)) != MAX_ELEM_VALUE:
            return False
    return True


def is_max_min_transitive(relation: FuzzySet):
    if not is_u_times_u_relation(relation):
        return False
    for (x, y0) in relation.get_domain():
        for (y1, z) in relation.get_domain():
            if (y0 == y1) and (relation.get_value_at((x, z)) <
                                   min(relation.get_value_at((x, y0)), relation.get_value_at((y1, z)))):
                return False
    return True


def composition_of_binary_relations(r1: FuzzySet, r2: FuzzySet):
    if (not is_u_times_u_relation(r1)) or (not is_u_times_u_relation(r2)):
        raise ValueError('Both relations have to be 2-dimensional!')
    u_first = r1.get_domain().get_first()[FIRST_DIM]
    u_last = r1.get_domain().get_last()[FIRST_DIM]

    y_first = r1.get_domain().get_first()[SECOND_DIM]
    y_last = r1.get_domain().get_last()[SECOND_DIM]
    y1_first = r2.get_domain().get_first()[FIRST_DIM]
    y1_last = r2.get_domain().get_last()[FIRST_DIM]

    if (y_first != y1_first) or (y_last != y1_last):
        raise ValueError('Second dimension of first relation must be ' +
                         'defined on the same set as the first dimension ' +
                         'of the second set!')

    w_first = r2.get_domain().get_first()[SECOND_DIM]
    w_last = r2.get_domain().get_last()[SECOND_DIM]

    d_new = Domain.combine(Domain.int_range(u_first, u_last + 1), Domain.int_range(w_first, w_last + 1))
    r_new = MutableFuzzySet(d_new)
    for (x, z) in d_new:
        r_new.set((x, z),
                  max(min(r1.get_value_at((x, y)), r2.get_value_at((y, z))) for y in range(y_first, y_last + 1)))

    return r_new


def is_fuzzy_equivalence(r: FuzzySet):
    return is_reflexive(r) and is_symmetric(r) and is_max_min_transitive(r)

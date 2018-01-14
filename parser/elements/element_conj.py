from enum import Enum

from parser.elements.element import Element


class Conjunction(Enum):
    I = 1
    ILI = 2


class ElementConjunction(Element):
    def __init__(self, conj: str):
        self.conj = Conjunction[conj]

    def __repr__(self):
        return self.conj.name

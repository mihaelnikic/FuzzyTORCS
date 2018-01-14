from parser.elements.element import Element


class ElementModifier(Element):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name

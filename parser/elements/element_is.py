from parser.elements.element import Element


class ElementIsNot(Element):
    def __init__(self, is_flag):
        self.is_flag = True if is_flag == 'je' else False

    def __repr__(self):
        return str(self.is_flag)

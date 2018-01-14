import abc


class Node:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.children = []

    def get_child(self, index):
        return self.children[index]

    def add_child_node(self, node):
        self.children.append(node)

    def number_of_children(self):
        return len(self.children)

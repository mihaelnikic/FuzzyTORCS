from enum import Enum

from fuzzy.domain.i_domain import Domain
from property.mods import ModifierProperty
from property.variable import VariableProperty


class ParamPropertyType(Enum):
    CONTROL = 1
    STATE = 2
    BOTH = 3


class ParameterProperty:
    def __init__(self, name: str, modifiers: list, type: str, variables: list, domain: Domain):
        self.name = name
        self.modifiers = dict((mod.name, mod) for mod in modifiers)
        self.type = ParamPropertyType[type]
        self.variables = dict((var.name, var) for var in variables)
        self.domain = domain

    def get_param_name(self) -> str:
        return self.name

    def get_modifier_by_name(self, mod_name: str) -> ModifierProperty:
        return self.modifiers[mod_name]

    def get_variable_by_name(self, var_name: str) -> VariableProperty:
        return self.variables[var_name]

    def get_domain(self) -> Domain:
        return self.domain

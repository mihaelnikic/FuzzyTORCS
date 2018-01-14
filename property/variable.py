from enum import Enum

from fuzzy.membership.gamma_function import GammaFunction
from fuzzy.membership.l_function import LFunction
from fuzzy.membership.lambda_function import LambdaFunction
from fuzzy.membership.pi_function import PiFunction

from fuzzy.i_unary import UnaryFunction
from fuzzy.membership.exactly_function import ExactlyFunction


class VariablePropertyFunction(Enum):
    L = LFunction
    LAMBDA = LambdaFunction
    GAMMA = GammaFunction
    EXACTLY = ExactlyFunction
    PI = PiFunction

class VariableProperty:
    def __init__(self, name, func, domain):
        self.name = name
        spltd = func.split()
        self.func = VariablePropertyFunction[spltd[0]].value(*[domain.index_of_element(float(arg)) for arg in spltd[1:]])

    def get_name(self):
        return self.name

    def get_function(self) -> UnaryFunction:
        return self.func

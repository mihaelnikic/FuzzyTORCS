import matplotlib.pyplot as plt
import numpy as np
from fuzzy.membership.gamma_function import GammaFunction
from fuzzy.membership.l_function import LFunction

from fuzzy.membership.lambda_function import LambdaFunction

if __name__ == "__main__":
    lambd = LambdaFunction(0.1, 0.2, 0.3)
    l = LFunction(0.3, 0.4)
    gamma = GammaFunction(0.3, 0.5)
    x = np.linspace(0, 1, 100)
    plt.figure(dpi=200)
    plt.plot(x, np.array([l(x) for x in x]))
    plt.show()
    plt.figure(dpi=200)
    plt.plot(x, np.array([lambd(x) for x in x]))
    plt.show()
    plt.figure(dpi=200)
    plt.plot(x, np.array([gamma(x) for x in x]))
    plt.show()
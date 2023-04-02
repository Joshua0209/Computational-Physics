import numpy as np
from scipy.optimize import minimize


def find_the_minimum(x, dx):
    best_par = np.zeros(3)
    ### START YOUR CODE HERE ###

    def func(t, target):
        a, b, c = target
        return a+b*t+c*t**2

    def chisq(target):
        t = np.linspace(0, 9, 10)
        return np.sum(((func(t, target)-x)/dx)**2)

    x_init = np.array([0.5, 0.5, 0.5])

    res = minimize(chisq, x_init)
    best_par = res.x
    #### END YOUR CODE HERE ####
    return best_par

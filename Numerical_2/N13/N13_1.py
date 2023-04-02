import numpy as np
from scipy.optimize import minimize


def find_the_minimum(a, b, c):
    min_x = 5.
    ### START YOUR CODE HERE ###

    def func(x):
        return np.sin(a*x) + np.cos(b*x) + c*x

    bounds = []
    h = min(abs(2*np.pi/a), abs(2*np.pi/b))
    n = int(10//h) + 1
    tmp = np.linspace(0, 10, n+1)
    bounds = [[(tmp[i], tmp[i+1])] for i in range(n)]
    x0 = [(tmp[i]+tmp[i+1])/2 for i in range(n)]
    min_value = func(min_x)
    for i in range(n):
        res = minimize(func, x0=x0[i], bounds=bounds[i])
        if min_value > res.fun:
            min_value = res.fun
            min_x = res.x

    min_x = float(min_x)
    #### END YOUR CODE HERE ####
    return min_x

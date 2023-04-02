import numpy as np
from scipy.optimize import root_scalar


def func(x, t):
    f_value = 0.
    ### START YOUR CODE HERE ###
    f_value = abs(np.sin(x)/((x/(2*np.pi))**x+np.pi/8)) - \
        x/(2*np.pi) + (x/(2*np.pi))**2-t/4
    #### END YOUR CODE HERE ####
    return float(f_value)


def find_the_roots(t):
    solutions = []
    ### START YOUR CODE HERE ###
    x = 0
    for x0 in np.linspace(0, 10, 1000):
        try:
            sol = root_scalar(func, args=(t,), x0=x0,
                              method='brentq', bracket=[x, x0])
        except ValueError:
            continue
        x = x0
        root = sol.root
        if not any(abs(root - sol) < 1e-6 for sol in solutions):
            solutions.append(root)
        if len(solutions) == 5:
            break
    #### END YOUR CODE HERE ####
    return np.array(solutions)


print(find_the_roots(t=+2.130929))

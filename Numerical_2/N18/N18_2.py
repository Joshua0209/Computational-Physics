import numpy as np


def func_integration(P, Q):
    result = 0.
    ### START YOUR CODE HERE ###

    def func(x, y, z):
        return np.sin((x+y)/P)*np.sin((y+z)/P)*np.sin((z+x)/P)/np.exp(-x*y*z/Q)

    nsamples = 10000000
    v = np.random.uniform(0, np.pi, (nsamples, 3))
    val = func(v[:, 0], v[:, 1], v[:, 2])
    result = val.sum()*np.pi**3 / v.shape[0]
    #### END YOUR CODE HERE ####
    return float(result)

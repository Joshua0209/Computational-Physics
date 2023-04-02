import numpy as np


def generate_dist(a, b):
    data = np.zeros(20000)
    ### START YOUR CODE HERE ###

    def func(x, y):
        return x*y*(1-a*x)*(1-b*y)
    nsamples = 1000000
    x = np.random.rand(nsamples)
    y = np.random.rand(nsamples)
    z = np.random.rand(nsamples)
    choice = z < func(x, y)
    data = np.hstack((x[choice][:10000], y[choice][:10000]))
    #### END YOUR CODE HERE ####
    return data

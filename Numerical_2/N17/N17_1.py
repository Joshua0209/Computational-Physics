import numpy as np


def generate_dist(a):
    data = np.zeros(10000)
    ### START YOUR CODE HERE ###

    def func(x):
        return 1/(1+a*x)

    x = np.random.rand(100000)
    y = np.random.rand(100000)
    data = x[y < func(x)][:10000]
    #### END YOUR CODE HERE ####
    return data

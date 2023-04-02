import numpy as np


def generate_dist(T, S):
    data = np.zeros(10000)
    ### START YOUR CODE HERE ###
    x = np.random.rand(10000)
    y = np.random.rand(10000)
    z = np.random.rand(10000)
    x = -T*np.log(1-x)
    r = (-2*np.log(y))**0.5
    phi = 2*np.pi*z
    data = S*x*r*np.cos(phi) + x
    #### END YOUR CODE HERE ####
    return data

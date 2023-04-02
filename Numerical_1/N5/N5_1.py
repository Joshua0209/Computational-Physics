import numpy as np


def give_me_an_array(n):
    output = np.zeros((10, 10), dtype='int64')
    ### START YOUR CODE HERE ###
    output = np.array([[0, n, 0, 0, 0, 0, 0, 0, n, 0],
                       [n, 0, n, 0, 0, 0, 0, n, 0, n],
                       [0, n, 0, n, 0, 0, n, 0, n, 0],
                       [0, 0, n, 0, n, n, 0, n, 0, 0],
                       [0, 0, 0, n, n, n, n, 0, 0, 0],
                       [0, 0, 0, n, n, n, n, 0, 0, 0],
                       [0, 0, n, 0, n, n, 0, n, 0, 0],
                       [0, n, 0, n, 0, 0, n, 0, n, 0],
                       [n, 0, n, 0, 0, 0, 0, n, 0, n],
                       [0, n, 0, 0, 0, 0, 0, 0, n, 0]])
    #### END YOUR CODE HERE ####
    return output

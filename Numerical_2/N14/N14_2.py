import numpy as np


def best_threshold(A, B):
    T = 0.
    ### START YOUR CODE HERE ###

    def loss(T):
        return np.count_nonzero([A > T])+np.count_nonzero([B < T])
    best_loss = float('inf')
    for i in np.arange(-4, 4, 0.01):
        if best_loss > loss(i):
            best_loss = loss(i)
            T = i
    #### END YOUR CODE HERE ####
    return float(round(T, 2))

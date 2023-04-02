import numpy as np


def best_bounds(A, B):
    bounds = np.array([-1., 1.])
    ### START YOUR CODE HERE ###

    def accuracy(bounds):
        NA = np.count_nonzero(np.where((A > bounds[0]) & (A < bounds[1])))
        NB = np.count_nonzero(np.where((B > bounds[0]) & (B < bounds[1])))
        if NA + NB == 0:
            return 0
        return NA/(NA+NB)**0.5
    best_acc = 0
    for L in np.arange(-3, 1, 0.1):
        for U in np.arange(-1, 3, 0.1):
            if L < U:
                if best_acc < accuracy([L, U]):
                    best_acc = accuracy([L, U])
                    bounds = np.array([L, U])
    #### END YOUR CODE HERE ####
    return bounds

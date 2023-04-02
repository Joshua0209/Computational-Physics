import numpy as np


def get_covariance(X, Y):
    covariance = np.ones((2, 2))
    ### START YOUR CODE HERE ###
    X -= X.mean()
    Y -= Y.mean()
    tmp = np.array([X, Y])
    for i in range(2):
        for j in range(2):
            covariance[i, j] = (tmp[i]*tmp[j]).mean()
    #### END YOUR CODE HERE ####
    return covariance

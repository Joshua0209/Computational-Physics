import numpy as np


def calc_image_features(A):
    S = np.zeros(3)
    ### START YOUR CODE HERE ###
    S[0] = np.sum((A-np.flip(A, 1))**2)
    S[1] = np.sum((A-np.flip(A, 0))**2)
    S[2] = np.sum((A-np.rot90(A))**2)
    #### END YOUR CODE HERE ####
    return S

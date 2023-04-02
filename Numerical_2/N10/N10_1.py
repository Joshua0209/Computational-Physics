import numpy as np


def give_me_a_matrix(A, B, C):
    output = np.zeros_like(A)
    ### START YOUR CODE HERE ###
    output = A@A + B@B + C@C - A@B - B@C - C@A + 4*np.eye(len(A))
    #### END YOUR CODE HERE ####
    return output

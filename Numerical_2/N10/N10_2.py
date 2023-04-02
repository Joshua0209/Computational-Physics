import numpy as np
import scipy.linalg as linalg


def give_me_a_matrix(A, B, C):
    output = np.zeros((2, 2))
    ### START YOUR CODE HERE ###
    output[0, 0] = linalg.det(A + B@linalg.inv(C))
    output[0, 1] = linalg.det(B - C@linalg.inv(A))
    output[1, 0] = linalg.det(B - A@linalg.inv(C))
    output[1, 1] = linalg.det(A + C@linalg.inv(B))
    #### END YOUR CODE HERE ####
    return output

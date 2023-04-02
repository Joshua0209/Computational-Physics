import numpy as np


def give_me_an_array(A, B):
    output = np.array([])
    ### START YOUR CODE HERE ###
    tmp1 = np.vstack((A.T, B.T, A.T, B.T, A.T)).T
    tmp2 = np.vstack((B.T, A.T, B.T, A.T, B.T)).T
    output = np.vstack((tmp1, tmp2, tmp1, tmp2, tmp1))
    #### END YOUR CODE HERE ####
    return output


A = np.array([[3, 7, 6, 3, 3]])

B = np.array([[5, 3, 4, 0, 2]])

print(give_me_an_array(A, B))

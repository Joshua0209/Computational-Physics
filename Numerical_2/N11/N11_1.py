import numpy as np
import scipy.linalg as linalg


def solve_linear_equations(b):
    output = np.zeros_like(b)
    ### START YOUR CODE HERE ###

    def A_mat(n):
        A = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i == j:
                    A[i, j] = 2
                elif i < j:
                    A[i, j] = 1
        return A
    A = A_mat(len(b))
    output = linalg.solve(A, b)
    #### END YOUR CODE HERE ####
    return output

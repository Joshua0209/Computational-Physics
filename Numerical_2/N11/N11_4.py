import numpy as np
import scipy.linalg as linalg


def chisquare_search(Y):
    X = np.array([1.00, 2.00, 3.00, 4.00, 5.00])
    S = np.array([[0.62, 0.21, 0.12, 0.04, 0.09],
                  [0.21, 0.78, 0.32, 0.10, 0.12],
                  [0.12, 0.32, 0.69, 0.03, 0.15],
                  [0.04, 0.10, 0.03, 0.95, 0.20],
                  [0.09, 0.12, 0.15, 0.20, 0.83]])
    best_a, best_b = 0., 0.

    ### START YOUR CODE HERE ###
    def compute_chisquare(Y, a, b):
        chisq = 0.
        ### START YOUR CODE HERE ###
        fX = a*X+b
        chisq = (Y-fX)@linalg.inv(S)@(Y-fX).T
        #### END YOUR CODE HERE ####
        return float(chisq)

    best_chisq = float('inf')
    for a in np.linspace(-1, 1, 11):
        for b in np.linspace(-1, 1, 11):
            chisq = compute_chisquare(Y, a, b)
            if chisq < best_chisq:
                best_chisq = chisq
                best_a, best_b = a, b
    #### END YOUR CODE HERE ####
    return np.array([best_a, best_b])

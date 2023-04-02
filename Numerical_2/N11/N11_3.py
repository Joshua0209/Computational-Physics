import numpy as np
import scipy.linalg as linalg


def compute_chisquare(Y):
    X = np.array([1.00, 2.00, 3.00, 4.00, 5.00])
    S = np.array([[0.62, 0.21, 0.12, 0.04, 0.09],
                  [0.21, 0.78, 0.32, 0.10, 0.12],
                  [0.12, 0.32, 0.69, 0.03, 0.15],
                  [0.04, 0.10, 0.03, 0.95, 0.20],
                  [0.09, 0.12, 0.15, 0.20, 0.83]])
    chisq = 0.
    ### START YOUR CODE HERE ###
    fX = X+1
    chisq = (Y-fX)@linalg.inv(S)@(Y-fX).T
    #### END YOUR CODE HERE ####
    return float(chisq)

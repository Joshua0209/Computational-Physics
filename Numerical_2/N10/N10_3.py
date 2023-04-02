import numpy as np


def cov_to_corr(covariance):
    correlation = covariance.copy()
    ### START YOUR CODE HERE ###
    tr = np.diagonal(correlation)**0.5
    TR = np.outer(tr, tr)
    correlation = correlation/TR
    print(correlation)
    #### END YOUR CODE HERE ####
    return correlation

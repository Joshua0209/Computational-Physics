import numpy as np


def calc_fisher_weights(A, B):
    W = np.zeros(3)
    ### START YOUR CODE HERE ###

    def calc_image_features(A):
        S = np.zeros(3)
        S[0] = np.sum((A-np.flip(A, 1))**2)
        S[1] = np.sum((A-np.flip(A, 0))**2)
        S[2] = np.sum((A-np.rot90(A))**2)
        return S

    SA = np.array([calc_image_features(a) for a in A]).T
    SB = np.array([calc_image_features(b) for b in B]).T

    mu0, mu1 = SA.mean(axis=1), SB.mean(axis=1)
    cov0, cov1 = np.cov(SA), np.cov(SB)

    W = np.linalg.inv((cov1+cov0))@(mu1-mu0)
    norm = np.sqrt((W**2).sum())
    W /= -norm
    #### END YOUR CODE HERE ####
    return W

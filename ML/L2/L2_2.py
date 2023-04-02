import numpy as np


def calc_roc_curve(A, B):
    ROC = np.zeros((2, 51))
    ### START YOUR CODE HERE ###

    def calc_fisher_dist(A, B):
        FA = np.zeros(len(A))
        FB = np.zeros(len(B))
        Fmin = 0.
        Fmax = 0.

        ### START YOUR CODE HERE ###
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
            return W, SA, SB

        W, SA, SB = calc_fisher_weights(A, B)
        FA, FB = W@SA, W@SB
        Fmin = min(FA.min(), FB.min())
        Fmax = max(FA.max(), FB.max())

        #### END YOUR CODE HERE ####
        return FA, FB, float(Fmin), float(Fmax)

    FA, FB, Fmin, Fmax = calc_fisher_dist(A, B)
    thresholds = np.linspace(Fmin, Fmax, 51)[:, np.newaxis]
    FA, FB = FA[np.newaxis, :], FB[np.newaxis, :]
    effA = np.count_nonzero(FA > thresholds, axis=1)/len(A)
    effB = np.count_nonzero(FB > thresholds, axis=1)/len(B)
    ROC = np. array([effA, effB])
    #### END YOUR CODE HERE ####
    return ROC

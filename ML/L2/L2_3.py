import numpy as np


def calc_auc_value(A, B):
    AUC = 0.

    ### START YOUR CODE HERE ###
    def calc_roc_curve(A, B):
        ROC = np.zeros((2, 51))
        thresholds = np.linspace(0, 1, 101)[:, np.newaxis]
        A, B = A[np.newaxis, :], B[np.newaxis, :]
        effA = np.count_nonzero(A > thresholds, axis=1)/len(A[0])
        effB = np.count_nonzero(B > thresholds, axis=1)/len(B[0])
        ROC = np. array([effA, effB])
        return ROC

    ROC = calc_roc_curve(A, B)
    y, x = ROC[0, :], ROC[1, :]
    AUC = [0.5*abs(x[i+1] - x[i])*(y[i+1] + y[i]) for i in range(len(x)-1)]
    AUC = np.sum(AUC)
    #### END YOUR CODE HERE ####
    return float(AUC)

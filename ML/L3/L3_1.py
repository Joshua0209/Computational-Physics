import numpy as np
from sklearn import svm


def scan_over_svm_classifier(x_train, y_train, R, S):
    y_test = np.zeros(101)
    ### START YOUR CODE HERE ###
    clf = svm.SVC(kernel='linear', C=1.0)
    clf.fit(x_train, y_train)
    x_test = np.linspace(0, 1, 101)
    R_m, S_m = np.ones_like(x_test)*R, np.ones_like(x_test)*S
    x_test = np.vstack((R_m, S_m, x_test)).T
    y_test = clf.predict(x_test)
    #### END YOUR CODE HERE ####
    return y_test

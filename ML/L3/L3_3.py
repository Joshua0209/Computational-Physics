import numpy as np
from sklearn import svm


def train_and_deploy_svm_classifier(x_data, y_data):
    y_predict = np.zeros(1500)
    ### START YOUR CODE HERE ###

    def train_deploy(x1, y1, x2, y2, x3, y3):
        clfs = [svm.SVC(kernel='rbf', C=C).fit(x1, y1) for C in Cs]
        scores = [clf.score(x2, y2) for clf in clfs]
        best_clf = clfs[np.argmax(scores)]
        return best_clf.predict(x3)

    Cs = [0.5, 1., 2.]
    xA, xB, xC = x_data[:500], x_data[500:1000], x_data[1000:]
    yA, yB, yC = y_data[:500], y_data[500:1000], y_data[1000:]
    y_predict[:500] = train_deploy(xB, yB, xC, yC, xA, yA)
    y_predict[500:1000] = train_deploy(xC, yC, xA, yA, xB, yB)
    y_predict[1000:] = train_deploy(xA, yA, xB, yB, xC, yC)
    #### END YOUR CODE HERE ####
    return y_predict

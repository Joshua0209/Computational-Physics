import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


def polyline_model(C):
    model = Sequential()
    ### START YOUR CODE HERE ###
    model.add(Dense(6, activation='relu', input_dim=1))
    model.add(Dense(1, activation='relu'))

    B1 = np.linspace(0, -5, 6)
    W2 = np.zeros((6, 1))
    C = np.hstack((C, np.zeros(1)))
    for i in range(1, 7):
        tmp = 0
        for j in range(1, i):
            tmp += (i+B1[j-1])*W2[j-1, 0]
        W2[i-1, 0] = (C[i-1] - tmp) / (i + B1[i-1])
    model.layers[0].set_weights([np.ones((1, 6)), B1])
    model.layers[1].set_weights([W2, np.zeros((1))])
    #### END YOUR CODE HERE ####
    return model

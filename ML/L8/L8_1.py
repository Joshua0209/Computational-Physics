import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD


def loss_vs_bias(x_data, y_data):
    loss = np.zeros((4, 31))
    ### START YOUR CODE HERE ###
    model = Sequential()
    model.add(Dense(units=1, activation='sigmoid', input_dim=1))
    model.add(Dense(units=1, activation='sigmoid'))
    model.add(Dense(units=1, activation='sigmoid'))
    model.add(Dense(units=1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=SGD(lr=1.0))
    biases = np.linspace(-3, 3, 31)
    for j in range(4):
        for i in range(len(biases)):
            for k in range(4):
                if j == k:
                    model.layers[k].set_weights(
                        [np.ones((1, 1)), biases[i].reshape(1)])
                else:
                    model.layers[k].set_weights(
                        [np.ones((1, 1)), np.zeros((1))])
            loss[-j-1, i] = model.evaluate(x_data, y_data)
    #### END YOUR CODE HERE ####
    return loss

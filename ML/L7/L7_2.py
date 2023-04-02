import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Reshape, Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.regularizers import l2


def loss_vs_epoch(x_train, y_train, x_test, y_test, W1, W2):
    loss = np.zeros((2, 60))
    ### START YOUR CODE HERE ###
    model = Sequential()
    model.add(Reshape((196,), input_shape=(14, 14)))
    model.add(Dense(units=20, activation='sigmoid'))
    model.add(Dense(units=1, activation='sigmoid', kernel_regularizer=l2(0.1)))
    model.compile(loss='binary_crossentropy', optimizer=SGD(lr=1.0))
    model.layers[1].set_weights([W1, np.zeros((20,))])
    model.layers[2].set_weights([W2, np.zeros((1))])
    for i in range(60):
        model.fit(x_train, y_train, epochs=1, batch_size=100, shuffle=False)
        loss[0, i] = model.evaluate(x_train, y_train)
        loss[1, i] = model.evaluate(x_test, y_test)
    #### END YOUR CODE HERE ####
    return loss

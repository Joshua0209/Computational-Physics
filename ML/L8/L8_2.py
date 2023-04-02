import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Reshape, Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.optimizers import SGD


def build_network_model(x_train, y_train, x_test, W1, W2):
    y_predict = np.zeros((len(x_test), 1))

    ### START YOUR CODE HERE ###
    model = Sequential()
    model.add(Reshape((14, 14, 1), input_shape=(14, 14)))
    model.add(Conv2D(8, kernel_size=(5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=SGD(lr=0.1))
    model.layers[1].set_weights([W1, np.zeros((8,))])
    model.layers[4].set_weights([W2, np.zeros((1,))])
    model.fit(x_train, y_train, epochs=20, batch_size=100, shuffle=False)
    y_predict = model.predict(x_test)
    #### END YOUR CODE HERE ####
    return y_predict

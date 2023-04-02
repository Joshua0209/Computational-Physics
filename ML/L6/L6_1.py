import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Reshape, Dense
from tensorflow.keras.optimizers import SGD
import tensorflow as tf
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)


def build_network_model(x_train, y_train, x_test, W1, W2):
    y_predict = np.zeros((len(x_test), 1))
    ### START YOUR CODE HERE ###
    model = Sequential()
    model.add(Reshape((196,), input_shape=(14, 14)))
    model.add(Dense(units=20, activation='sigmoid'))
    model.add(Dense(units=1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=SGD(lr=1.0))
    model.layers[1].set_weights([W1, np.zeros((20,))])
    model.layers[2].set_weights([W2, np.zeros((1))])
    model.fit(x_train, y_train, epochs=20, batch_size=100, shuffle=False)
    y_predict = model.predict(x_test)
    #### END YOUR CODE HERE ####
    return y_predict

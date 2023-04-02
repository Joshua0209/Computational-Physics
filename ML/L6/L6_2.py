import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Reshape, Dense
from tensorflow.keras.optimizers import SGD


def softmax_output_ranking(x_train, y_train, W1, W2):
    counts = np.array([0, 0, 0, 0])
    ### START YOUR CODE HERE ###
    y_train_one_hot = np.array([np.eye(4)[y] for y in y_train])
    model = Sequential()
    model.add(Reshape((196,), input_shape=(14, 14)))
    model.add(Dense(units=20, activation='sigmoid'))
    model.add(Dense(units=4, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=1.0))
    model.layers[1].set_weights([W1, np.zeros((20,))])
    model.layers[2].set_weights([W2, np.zeros((4,))])
    model.fit(x_train, y_train_one_hot, epochs=20,
              batch_size=200, shuffle=False)
    y_predict = model.predict(x_train)
    for y_p, y in zip(y_predict, y_train):
        for i in range(len(y_p)):
            if np.argsort(y_p)[i] == y:
                counts[3-i] += 1

        #### END YOUR CODE HERE ####
    return counts

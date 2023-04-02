import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam


def build_network_model(source_string):
    ### START YOUR CODE HERE ###
    def string_to_onehot(input):
        output = np.zeros(27)
        if len(input) >= 2:
            output = np.zeros((len(input), 27))
        idx_to_alps = dict((chr(i+96), i) for i in range(1, 27))
        idx_to_alps[" "] = 0

        for i in range(len(input)):
            if len(input) >= 2:
                output[i, idx_to_alps[input[i]]] = 1
            else:
                output[idx_to_alps[input]] = 1

        return output

    x_train = np.zeros((100, 10, 27))
    y_train = np.zeros((100, 27))
    for i in range(len(x_train)):
        x_train[i] = string_to_onehot(source_string[i:i+10])
        y_train[i] = string_to_onehot(source_string[i+10])
    model = Sequential()
    model.add(LSTM(100, input_shape=(10, 27)))
    model.add(Dense(27, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='Adam')
    model.fit(x_train, y_train, epochs=100, batch_size=20, shuffle=False)
    #### END YOUR CODE HERE ####
    return model

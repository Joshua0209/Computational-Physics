import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Reshape, Dense


def image_generation(x_test, W1, W2, W3, B1, B2, B3):
    y_predict = np.zeros((100, 14, 14))

    ### START YOUR CODE HERE ###
    latent_size = 32
    img_shape = (14, 14)
    generator = Sequential()
    generator.add(Dense(64, input_dim=latent_size, activation='relu'))
    generator.add(Dense(128, activation='relu'))
    generator.add(Dense(np.prod(img_shape), activation='tanh'))
    generator.add(Reshape(img_shape))
    generator.layers[0].set_weights([W1, B1])
    generator.layers[1].set_weights([W2, B2])
    generator.layers[2].set_weights([W3, B3])
    y_predict = generator.predict(x_test)
    #### END YOUR CODE HERE ####
    return y_predict

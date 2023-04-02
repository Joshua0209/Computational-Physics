import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Reshape, Dense


def image_discrimination(x_train, x_test, W1, W2, W3, W4, W5, B1, B2, B3, B4, B5):
    score = np.zeros((2, 100))

    ### START YOUR CODE HERE ###
    latent_size = 32
    img_shape = (14, 14)

    generator = Sequential()
    generator.add(Dense(64, input_dim=latent_size, activation='relu'))
    generator.add(Dense(128, activation='relu'))
    generator.add(Dense(np.prod(img_shape), activation='tanh'))
    generator.add(Reshape(img_shape))

    discriminator = Sequential()
    discriminator.add(Reshape((np.prod(img_shape),), input_shape=img_shape))
    discriminator.add(Dense(64, activation='relu'))
    discriminator.add(Dense(1, activation='sigmoid'))

    generator.layers[0].set_weights([W1, B1])
    generator.layers[1].set_weights([W2, B2])
    generator.layers[2].set_weights([W3, B3])
    discriminator.layers[1].set_weights([W4, B4])
    discriminator.layers[2].set_weights([W5, B5])

    y_predict = generator.predict(x_test)
    score[0, :] = discriminator.predict(y_predict).reshape(100, 1)
    score[1, :] = discriminator.predict(x_train).reshape(100, 1)
    #### END YOUR CODE HERE ####
    return score

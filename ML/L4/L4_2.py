import numpy as np


def sigma(z):
    return 0.5*(np.tanh(0.5*z)+1.)


def sigma_p(z):
    return sigma(z)*(1.-sigma(z))


class neurons(object):
    def __init__(self, shape):
        self.shape = shape
        self.v = [np.zeros((n, 1)) for n in shape]
        self.z = [np.zeros((n, 1)) for n in shape[1:]]
        self.w = [np.ones((n, m)) for n, m in zip(shape[1:], shape[:-1])]
        self.b = [np.zeros((n, 1)) for n in shape[1:]]

    def predict(self, x):
        self.v[0] = x.reshape(self.v[0].shape)
        for l in range(len(self.shape)-1):
            self.z[l] = np.dot(self.w[l], self.v[l])+self.b[l]
            self.v[l+1] = sigma(self.z[l])
        return self.v[-1]


def calc_fully_connected_NN(x_data, y_data):
    loss = np.zeros(201)
    ### START YOUR CODE HERE ###
    model = neurons([1, 8, 1, 8, 1])
    Bs = np.linspace(-10., 10., 201)
    for i in range(len(Bs)):
        model.b[1] = Bs[i]
        t = np.array([model.predict(x) for x in x_data]).reshape(-1)
        loss[i] = ((t-y_data)**2).mean() / 2.
    #### END YOUR CODE HERE ####
    return loss

import numpy as np


def sigma(z):
    return 0.5*(np.tanh(0.5*z)+1.)


def sigma_p(z):
    return sigma(z)*(1.-sigma(z))


class neurons(object):
    def __init__(self, shape, W):
        self.shape = shape
        self.v = [np.zeros((n, 1)) for n in shape]
        self.z = [np.zeros((n, 1)) for n in shape[1:]]
        self.w = [np.ones((n, m))*W for n, m in zip(shape[1:], shape[:-1])]
        self.b = [np.ones((n, 1)) for n in shape[1:]]
        self.delw = [np.zeros(w.shape) for w in self.w]
        self.delb = [np.zeros(b.shape) for b in self.b]

    def predict(self, x):
        self.v[0] = x.reshape(self.v[0].shape)
        for l in range(len(self.shape)-1):
            self.z[l] = np.dot(self.w[l], self.v[l])+self.b[l]
            self.v[l+1] = sigma(self.z[l])
        return self.v[-1]

    def gradient(self, y):
        for l in range(len(self.shape)-2, -1, -1):
            if l == len(self.shape)-2:
                delta = (self.v[-1]-y.reshape(self.v[-1].shape)
                         )*sigma_p(self.z[l])
            else:
                delta = np.dot(
                    self.w[l+1].T, self.delb[l+1])*sigma_p(self.z[l])
            self.delb[l] = delta
            self.delw[l] = np.dot(delta, self.v[l].T)


def calc_NN_gradients(x_data, y_data, W):
    grad = np.zeros(10)
    ### START YOUR CODE HERE ###
    model = neurons([4, 10, 4], W)
    model.b[0] = np.linspace(0, 0.9, 10)[:, np.newaxis]
    sum_delw = [np.zeros(w.shape) for w in model.w]
    sum_delb = [np.zeros(b.shape) for b in model.b]
    model.predict(x_data)
    model.gradient(y_data)
    for l in range(len(model.shape)-1):
        sum_delw[l] += model.delw[l]
        sum_delb[l] += model.delb[l]
    grad = sum_delb[0].reshape(-1)
    #### END YOUR CODE HERE ####
    return grad

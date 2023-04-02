import numpy as np


def func_integration(A, B, C):
    result = 0.
    ### START YOUR CODE HERE ###

    def func(r, theta, phi):
        return A*r**3+B*r**2*np.sin(theta)*np.sin(phi)+C*r*np.cos(theta)*np.cos(phi)

    nsamples = 10000000
    v = np.random.rand(nsamples, 3)*2 - 1
    r = (v[:, 0]**2 + v[:, 1]**2 + v[:, 2]**2)**0.5
    v = v[np.vstack((r < 1, r < 1, r < 1)).T].reshape((-1, 3))
    r = r[r < 1]
    theta = np.arctan((v[:, 0]**2 + v[:, 1]**2)**0.5/v[:, 2])
    phi = np.arctan2(v[:, 1], v[:, 0])
    v = np.vstack((r, theta, phi)).T
    val = func(v[:, 0], v[:, 1], v[:, 2])
    result = val.sum()*4/3*np.pi / v.shape[0]

    #### END YOUR CODE HERE ####
    return float(result)

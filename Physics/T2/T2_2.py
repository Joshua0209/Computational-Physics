import matplotlib.pyplot as plt
import numpy as np


def Lyapunov_coeff(mu):
    Lambda = 0.

    ### START YOUR CODE HERE ###

    n = 500
    # vlam, vmu = [], []
    # mu = 2.5
    # while mu < 4.0:
    x, lam = 0.5, 0.
    for i in range(n):
        lam += np.log(np.abs((1-mu*x)*np.exp(mu*(1.-x))))
        x = x*np.exp(mu*(1.-x))
    lam /= n
    Lambda = lam
    # vlam.append(lam)
    # vmu.append(mu)
    # mu += 0.01

    # plt.plot([2.5, 4.0], [0., 0.], lw=2, c='gray')
    # plt.plot(vmu, vlam, lw=2)
    # plt.ylim(-1., 1)
    # plt.xlabel('mu', size=18)
    # plt.ylabel('lambda', size=18)
    # plt.show()
    #### END YOUR CODE HERE ####
    return float(Lambda)

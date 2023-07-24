import numpy as np
import matplotlib.pyplot as plt


def bifurcations_ecology_map():
    data = np.zeros(8000)

    ### START YOUR CODE HERE ###
    vx, vmu = [], []
    mu = 1.80
    while mu <= 2.59:
        x = 0.5
        for n in range(200):
            x = x*np.exp(mu*(1.-x))
        for n in range(100):
            x = x*np.exp(mu*(1.-x))
            vx.append(x)
            vmu.append(mu)
        mu += 0.01

    data = np.array(vx)
    # plt.scatter(vmu, vx, marker='.', s=1.0)
    # plt.xlabel('mu', size=18)
    # plt.ylabel('x*', size=18)
    # plt.show()
    #### END YOUR CODE HERE ####
    return data

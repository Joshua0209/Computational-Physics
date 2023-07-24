import numpy as np
import matplotlib.pyplot as plt


def averge_food_counter(sigma):
    result = 0.
    ### START YOUR CODE HERE ###
    for i in range(400):
        food = np.random.uniform(-1, 1, (100, 2))
        protist = np.array([0, 0])
        loc = np.array([0, 0])
        cnt = np.zeros(100)
        for _ in range(100):
            R = np.abs(np.random.normal(0, sigma, 1))
            cnt[(np.sum((food - protist)**2, axis=1)) < R**2] = 1

            phi = np.random.uniform(0, 2*np.pi, 1)
            tmp = protist + np.hstack([R*np.cos(phi), R*np.sin(phi)])
            loc = np.vstack([loc, tmp])
            if np.all(np.abs(tmp) <= 1):
                protist = tmp
        result += np.sum(cnt)
        # plt.scatter(loc[:, 0], loc[:, 1], c='r')
        # plt.scatter(food[:, 0], food[:, 1], c='b')
        # plt.show()
    result /= 400

    #### END YOUR CODE HERE ####
    return float(result)


print(averge_food_counter(0.2400))

import numpy as np
import matplotlib.pyplot as plt


def give_me_a_line(c):
    output = plt.plot([], [])
    ### START YOUR CODE HERE ###
    x = np.linspace(0, 1, 101)
    X = np.apply_along_axis(lambda i: np.array(
        [x**i for i in range(len(c))]), 0, x).T
    y = X@c
    output = plt.plot(x, y)
    #### END YOUR CODE HERE ####
    return output[0]


c = np.array([1, 1, 1])
print(give_me_a_line(c))

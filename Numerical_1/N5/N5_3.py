import numpy as np


def give_me_an_array(x):
    output = np.ones_like(x)
    ### START YOUR CODE HERE ###

    def func(x):
        value = 1.
        for i in range(1, 5):
            value *= np.cos(i*np.pi*x/2)*np.cosh(x) + \
                np.sin(i*np.pi*x/2)*np.sinh(x)
        return value
    output = np.apply_along_axis(func, 0, x)
    #### END YOUR CODE HERE ####
    return output


x = np.array([0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9])
print(give_me_an_array(x))

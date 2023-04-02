import math


def func(x):
    value = 1.
    ### START YOUR CODE HERE ###
    for i in range(1, 5):
        value *= math.cos(i*math.pi*x/2)*math.cosh(x) + \
            math.sin(i*math.pi*x/2)*math.sinh(x)
        #### END YOUR CODE HERE ####
    return value


def func_first_derivative(x):
    value = 1.
    ### START YOUR CODE HERE ###
    h = 10E-3
    value = (8*func(x+h/4)-8*func(x-h/4)-func(x+h/2)+func(x-h/2))/(3*h)
    #### END YOUR CODE HERE ####
    return value

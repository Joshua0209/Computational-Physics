import math


def func(n, x):
    value = 0.
    ### START YOUR CODE HERE ###
    for i in range(n+1):
        value += x**i
    #### END YOUR CODE HERE ####
    return value


def func_integrated_numerical(n):
    value = 0.
    ### START YOUR CODE HERE ###
    h = 10E-4
    min, max = -1., 1.

    for i in range(int((max-min)/h)):
        f0, f1 = func(n, min+h*(i+1)), func(n, min+h*i)
        value += (f0 + f1)/2*h
    #### END YOUR CODE HERE ####
    return value


def func_integrated_analytical(n):
    value = 0.
    ### START YOUR CODE HERE ###
    for i in range(n+1):
        if (i+1) % 2 != 0:
            value += 2/(i+1)
    #### END YOUR CODE HERE ####
    return value

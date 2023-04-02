import math


def func(x):
    value = 1.
    ### START YOUR CODE HERE ###
    value = x**2 + math.e**x + math.log(x)+math.sin(x)
    #### END YOUR CODE HERE ####
    return value


def func_2nd_derivative_numerical(x):
    value = 1.
    ### START YOUR CODE HERE ###
    h = 10E-4
    value = (func(x+h)+func(x-h)-2*func(x))/(h**2)
    #### END YOUR CODE HERE ####
    return value


def func_2nd_derivative_analytical(x):
    value = 1.
    ### START YOUR CODE HERE ###
    value = 2 + math.e**x - 1/x**2 - math.sin(x)
    #### END YOUR CODE HERE ####
    return value

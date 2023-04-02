import scipy.integrate as integrate
import math


def convoluted_BreitWigner(E, M, Gamma, sigma):
    value = 0.
    ### START YOUR CODE HERE ###

    def f(E, M, Gamma):
        return 1/((E**2-M**2)**2 + M**2*Gamma**2)

    def func(x, E, M, Gamma):
        return f(E-x, M, Gamma)*math.e**(-x**2/(2*sigma**2))
    value = integrate.quadrature(
        func, -3*sigma, 3*sigma, tol=1E-10, rtol=1E-10, args=(E, M, Gamma), maxiter=1000)
    value = float(value[0])
    #### END YOUR CODE HERE ####
    return value

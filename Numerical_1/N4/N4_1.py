import scipy.integrate as integrate
import math


def prob_at_nsigma(n):
    prob = 0.
    ### START YOUR CODE HERE ###

    def func(x):
        sigma, mu = 1., 0.
        return 1/(sigma*math.sqrt(2*math.pi))*math.e**(-(x-mu)**2/(2*sigma**2))
    prob = integrate.quadrature(func, -n, n, tol=1E-10, rtol=1E-10)
    prob = float(prob[0])
    #### END YOUR CODE HERE ####
    return prob

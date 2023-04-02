import numpy as np
from scipy.optimize import minimize


def bestfit_parameters(vy):
    best_par = np.zeros(3)
    ### START YOUR CODE HERE ###

    def f(x, tau):
        return np.exp(-x/tau)

    def g(x, mu, sigma):
        return np.exp(-(x-mu)**2/2/sigma**2)

    def F(x, target):
        tau, mu, sigma, M, N = target
        return M*g(x, mu, sigma) + N*f(x, tau)

    def chisq(target):
        return np.sum((F(vx, target) - vy)**2/vyerr**2)

    vx = np.linspace(0.01, 1.99, 100)
    vyerr = vy**0.5
    x_init = np.array([1.5, 1., 0.05, 10., 5.])
    res = minimize(chisq, x_init)
    best_par = res.x[:3]

    #### END YOUR CODE HERE ####
    return best_par

import numpy as np
from scipy.integrate import solve_ivp


def charge_on_capacitor(R, C, V, T):
    charge = np.zeros(8)
    ### START YOUR CODE HERE ###

    def RC(t, Y):
        return np.array([V*np.exp(-t/T)/R - Y/R/C])
    Y = np.zeros(1)
    res = solve_ivp(RC, [0, 8], Y, rtol=1e-10,
                    atol=1e-10, t_eval=np.linspace(1, 8, 8))
    charge = res.y.T.reshape(-1)
    #### END YOUR CODE HERE ####
    return charge

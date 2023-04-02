import numpy as np
from scipy.integrate import solve_ivp


def current_on_circuit(R, L, C, I0):
    current = np.zeros(8)
    ### START YOUR CODE HERE ###

    def RLC(t, Y):
        I, Ip = Y
        Ipp = -R/L*Ip - I/L/C
        return np.array([Ip, Ipp])

    Y = np.array([I0, 0])
    res = solve_ivp(RLC, [0, 8], Y, rtol=1e-10,
                    atol=1e-10, t_eval=np.linspace(1, 8, 8))
    current = res.y[:1].T.reshape(-1)
    #### END YOUR CODE HERE ####
    return current

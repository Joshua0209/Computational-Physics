import numpy as np
from scipy.integrate import solve_ivp


def particle_positions(E, B):
    positions = np.zeros(24)
    ### START YOUR CODE HERE ###

    def EM_field(t, Y):
        X, V = Y[:3], Y[3:]
        A = q/m*(E+np.cross(V, B))
        return np.array([V, A]).reshape(-1)
    m, q = 1., 1.
    Y = np.zeros(6)
    res = solve_ivp(EM_field, [0, 8], Y, rtol=1e-10,
                    atol=1e-10, t_eval=np.linspace(1, 8, 8))
    positions = res.y[:3].T.reshape(-1)
    #### END YOUR CODE HERE ####
    return positions


E = np.array([0.28049797, 0.14561325, - 0.16127501])
B = np.array([0.4727921, 0.24079647, - 0.05382949])
print(particle_positions(E, B))

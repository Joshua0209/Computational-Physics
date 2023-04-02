import numpy as np
from scipy.integrate import solve_ivp


def ironball_position(theta, v0, k, deltat):
    position = np.zeros(2)
    ### START YOUR CODE HERE ###

    def cannon(t, Y):
        x, y, vx, vy = Y
        v = np.sqrt(vx**2+vy**2)
        return np.array([vx, vy, -k*v**2/m*vx/v, -k*v**2/m*vy/v-g])

    m, g = 1., 9.8
    Y = np.array([0., 0., v0*np.cos(theta), v0*np.sin(theta)])
    position = solve_ivp(cannon, [0, deltat], Y).y[:, -1][:2]
    #### END YOUR CODE HERE ####
    return position

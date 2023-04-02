import numpy as np
from scipy.integrate import solve_ivp


def twobody_positions(x1, y1, x2, y2, deltat):
    positions = np.zeros(4)
    ### START YOUR CODE HERE ###

    def twobody(t, Y):
        x1, y1, x2, y2, vx1, vy1, vx2, vy2 = Y
        L = ((x1-x2)**2+(y1-y2)**2)**0.5
        ax1 = k/m1 * (L - L0) * (x2 - x1)/L
        ay1 = k/m1 * (L - L0) * (y2 - y1)/L
        ax2 = k/m2 * (L - L0) * (x1 - x2)/L
        ay2 = k/m2 * (L - L0) * (y1 - y2)/L
        return np.array([vx1, vy1, vx2, vy2, ax1, ay1, ax2, ay2])

    L0, k, m1, m2 = 1., 100., 0.5, 1.
    Y = np.array([x1, y1, x2, y2, 0., 0., 0., 0.])
    res = solve_ivp(twobody, [0., deltat], Y, rtol=1e-10, atol=1e-10)
    positions = res.y[:, -1][:4]
    #### END YOUR CODE HERE ####
    return positions

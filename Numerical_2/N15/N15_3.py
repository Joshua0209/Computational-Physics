import numpy as np
from scipy.integrate import solve_ivp

# in the order of [mass, x, y, vx, vy]
init_data = np.array([[0.362, +0.380, -1.954, -2.364, +0.461],
                      [0.168, +0.032, +0.631, +0.233, -0.608],
                      [0.413, +0.280, -0.095, -0.672, -0.369],
                      [0.209, -1.669, +0.116, -1.965, +0.237],
                      [0.172, +0.376, +0.673, -0.370, +0.723],
                      [0.322, -0.583, +0.355, -0.405, +0.831],
                      [0.289, -0.619, -0.960, -0.525, -1.366],
                      [0.108, +0.626, -1.931, +0.276, +1.698],
                      [0.491, +0.499, +0.217, -1.237, +0.084],
                      [0.325, +0.781, +1.452, -0.295, -0.827]])


def multibody_positions(deltat):
    positions = np.zeros(20)
    ### START YOUR CODE HERE ###

    def multibody(t, Y):
        n = int(len(Y)//4)
        x, y, vx, vy = Y[:n], Y[n:2*n], Y[2*n:3*n], Y[3*n:4*n]
        R = ((x-x[:, np.newaxis])**2+(y-y[:, np.newaxis])**2)**0.5
        np.fill_diagonal(R, np.inf)

        ax, ay = np.zeros_like(vx), np.zeros_like(vy)
        for i in range(n):
            ax[i] = np.inner(((x-x[i])/R[i]**3), mass)
            ay[i] = np.inner(((y-y[i])/R[i]**3), mass)
        return np.array([vx, vy, ax, ay]).reshape(-1)

    mass = init_data[:, 0].reshape(-1)
    Y = init_data[:, 1:].T.reshape(-1)
    res = solve_ivp(multibody, [0., deltat], Y, rtol=1e-10, atol=1e-10)
    positions = res.y[:, -1][:20]
    #### END YOUR CODE HERE ####
    return positions

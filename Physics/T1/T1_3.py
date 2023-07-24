import matplotlib.pyplot as plt
import numpy as np


def groundstate_energy(V0, Xm):
    E0 = 0.

    ### START YOUR CODE HERE ###
    E = -82.      # energy in MeV
    L = 2.        # boundary in fm
    # V0 = 83.      # potential in MeV
    conv = 0.0483  # 2m/hbar^2, m = 940 MeV/c^2, hbar*c = 197.32 MeV*fm
    x_min, x_max = -2*L, +2*L   # lower/upper bound
    # x_match = L*0.7             # match location
    x_match = Xm

    def V(x):
        return (np.abs(x) <= L)*(-1+np.abs(x)/L)*V0

    def f(x, y):
        psi = y[0]
        psip = y[1]
        psipp = -conv*(E-V(x))*psi
        return np.array([psip, psipp])

    def solve_rk4(x0, x1, y, h):
        x = x0
        psi = []
        while (x-x0)*(x-x1) <= 1E-7:
            psi.append((x, y[0], y[1]))
            k1 = f(x, y)
            k2 = f(x+0.5*h, y+0.5*h*k1)
            k3 = f(x+0.5*h, y+0.5*h*k2)
            k4 = f(x+h, y+h*k3)
            y += h/6.*(k1+2.*k2+2.*k3+k4)
            x += h
        return np.array(psi)

    rec = []
    while E < 0.:
        kappa = (conv*abs(E))**0.5  # wave vector

        x = x_min
        y = np.array([np.exp(kappa*x), kappa*np.exp(kappa*x)])
        psi_L = solve_rk4(x, x_match, y, +0.01)

        x = x_max
        y = np.array([np.exp(-kappa*x), -kappa*np.exp(-kappa*x)])
        psi_R = solve_rk4(x, x_match, y, -0.01)

        delta = (psi_L[-1, 2]/psi_L[-1, 1]-psi_R[-1, 2]/psi_R[-1, 1]) / \
                (psi_L[-1, 2]/psi_L[-1, 1]+psi_R[-1, 2]/psi_R[-1, 1])
        # print('E = ', E, ' x_match = ', x_match, ' delta = %+f' % delta)
        rec.append((E, delta))
        if len(rec) > 1:
            if rec[-2][1]*delta < 0 and len(rec) != 1:
                if abs(rec[-2][1]) < abs(delta):
                    E0 = rec[-2][0]
                else:
                    E0 = E
                break
        E += 1.
    # rec = np.array(rec)

    # plt.figure(figsize=(8, 6), dpi=80)
    # plt.plot([-V0, 0.], [0., 0.], lw=2, c='gray')
    # plt.plot(rec[:, 0], rec[:, 1], ls='None', marker='o')
    # plt.ylim(-8., 8.)
    # plt.show()
    #### END YOUR CODE HERE ####
    return float(E0)


print(groundstate_energy(+66.227827, +0.000000))

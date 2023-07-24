import matplotlib.pyplot as plt
import numpy as np


def diff_log_derivative(V0, E, Xm):
    Delta = 0.

    ### START YOUR CODE HERE ###

    # E = -76.      # energy in MeV
    L = 2.        # boundary in fm
    # V0 = 83.      # potential in MeV
    conv = 0.0483  # 2m/hbar^2, m = 940 MeV/c^2, hbar*c = 197.32 MeV*fm
    x_min, x_max = -2*L, +2*L   # lower/upper bound
    kappa = (conv*abs(E))**0.5  # wave vector
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

    x = x_min
    y = np.array([np.exp(kappa*x), kappa*np.exp(kappa*x)])
    psi_L = solve_rk4(x, x_match, y, +0.001)

    x = x_max
    y = np.array([np.exp(-kappa*x), -kappa*np.exp(-kappa*x)])
    psi_R = solve_rk4(x, x_match, y, -0.001)

    delta = (psi_L[-1, 2]/psi_L[-1, 1]-psi_R[-1, 2]/psi_R[-1, 1]) / \
            (psi_L[-1, 2]/psi_L[-1, 1]+psi_R[-1, 2]/psi_R[-1, 1])
    # print('E = ', E, ' x_match = ', x_match, ' delta = ', delta)
    Delta = delta

    # plt.figure(figsize=(8, 6), dpi=80)
    # vx = np.linspace(x_min, x_max, 500)
    # vy = V(vx)
    # plt.plot(vx, vy, c='gray', lw=3)
    # plt.plot([x_match, x_match], [0., -V0], c='blue', lw=2, ls=':')
    # psi_max = max(psi_L[:, 1].max(), psi_R[:, 1].max())
    # plt.plot(psi_L[:, 0], psi_L[:, 1]/psi_max*V0*0.8-V0, lw=3, ls='--')
    # plt.plot(psi_R[:, 0], psi_R[:, 1]/psi_max*V0*0.8-V0, lw=3, ls='-.')
    # plt.show()
    #### END YOUR CODE HERE ####
    return float(Delta)

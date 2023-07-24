import matplotlib.pyplot as plt
import numpy as np


def calc_wave_function(V0, E):
    psi = np.zeros(801)

    ### START YOUR CODE HERE ###
    # E = -76.      # energy in MeV
    L = 2.        # boundary in fm
    # V0 = 83.      # potential in MeV
    conv = 0.0483  # 2m/hbar^2, m = 940 MeV/c^2, hbar*c = 197.32 MeV*fm
    x_min, x_max = -2*L, +2*L   # lower/upper bound
    kappa = (conv*abs(E))**0.5  # wave vector

    def V(x):
        return (np.abs(x) <= L)*(-1+np.abs(x)/L)*V0

    def f(x, y):
        psi = y[0]
        psip = y[1]
        psipp = -conv*(E-V(x))*psi
        return np.array([psip, psipp])

    h = 0.01
    x = x_min
    y = np.array([np.exp(kappa*x), kappa*np.exp(kappa*x)])
    psi_L = []
    while x < x_max:
        psi_L.append((x, y[0], y[1]))
        k1 = f(x, y)
        k2 = f(x+0.5*h, y+0.5*h*k1)
        k3 = f(x+0.5*h, y+0.5*h*k2)
        k4 = f(x+h, y+h*k3)
        y += h/6.*(k1+2.*k2+2.*k3+k4)
        x += h
    psi_L = np.array(psi_L)
    psi = psi_L[:, 1]

    # plt.figure(figsize=(8, 6), dpi=80)
    # vx = np.linspace(x_min, x_max, 500)
    # vy = V(vx)
    # plt.plot(vx, vy, c='gray', lw=3)
    # plt.plot(psi_L[:, 0],psi_L[:,1]/psi_L[:,1].max()*V0*0.8-V0,lw=3,ls='--')
    # plt.show()
    #### END YOUR CODE HERE ####
    return psi

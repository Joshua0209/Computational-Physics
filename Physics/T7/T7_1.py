import numpy as np
import matplotlib.pyplot as plt


def calc_heatflow_rate(TH, TL):
    H = np.zeros(49)

    ### START YOUR CODE HERE ###
    dx = 0.02
    N, L, dt, steps = 50, 1., 0.001, 1000
    K, C, rho = 1, 1, 10
    Coeff = K/C/rho
    x = np.linspace(0., L, N+1)
    t = np.array([i*dt for i in range(steps)])
    vx, vt = np.meshgrid(x, t)
    T = np.zeros((steps, N+1))
    T[0, :] = TL
    T[:, 0] = TH
    T[:, -1] = TL
    eta = Coeff*dt/(L/N)**2
    for j in range(0, steps-1):  # time
        for i in range(1, N):  # space
            T[j+1, i] = T[j, i] + eta*(T[j, i+1]+T[j, i-1]-T[j, i]*2.)

    H = -K*(T[-1, 2:]-T[-1, :N-1])/2/dx

    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # surf = ax.plot_surface(vx, vt, T, cmap='viridis')
    # ax.set_xlabel('x')
    # ax.set_ylabel('t')
    # ax.set_zlabel('T')
    # plt.show()
    #### END YOUR CODE HERE ####
    return H


print(calc_heatflow_rate(+42.1639, +25.2783))

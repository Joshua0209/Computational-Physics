import numpy as np
import matplotlib.pyplot as plt


def calc_wave_displacement(W):
    Y = np.zeros(201)

    ### START YOUR CODE HERE ###
    dx, L, v, dt, tf = 0.005, 1., 1.0, 0.002, 2
    steps, N = int(tf/dt)+1, int(L/dx)

    x = np.linspace(0., L, N+1)
    t = np.array([i*dt for i in range(steps)])
    vx, vt = np.meshgrid(x, t)
    y = np.zeros((steps, N+1))
    y[:, 0] = np.sin(W*np.linspace(0, tf, steps))
    eta = v**2/(L/N/dt)**2

    for i in range(1, N):  # first step
        y[1, i] = y[0, i] + 0.5*eta*(y[0, i+1]+y[0, i-1]-y[0, i]*2.)
    for j in range(1, steps-1):  # time
        for i in range(1, N):  # space
            y[j+1, i] = y[j, i]*2. - y[j-1, i] + \
                eta*(y[j, i+1]+y[j, i-1]-y[j, i]*2.)

    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # surf = ax.plot_surface(vx, vt, y, cmap='viridis')
    # ax.set_xlabel('x')
    # ax.set_ylabel('t')
    # ax.set_zlabel('y')
    # plt.show()
    Y = y[-1, :]
    #### END YOUR CODE HERE ####
    return Y


print(calc_wave_displacement(+3.5213))

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def calc_wave_displacement(S):
    Z = np.zeros((41, 41))

    ### START YOUR CODE HERE ###
    N, L, v, dt, tf = 40, 1., 1.0, 0.004, 1
    steps = int(tf/dt)+1
    global z
    z = np.zeros((3, N+1, N+1))
    eta = v**2/(L/N/dt)**2
    defect = np.zeros_like(Z)
    defect[int(L/4*N), int(L/4*N)] = defect[int(3*L/4*N), int(3*L/4*N)] \
        = defect[int(L/4*N), int(3*L/4*N)] = defect[int(3*L/4*N), int(L/4*N)] = 1
    defect = defect.astype(bool)
    for i in range(1, N):  # initial condition
        for j in range(1, N):
            z[0, j, i] = np.exp(-0.5*(i/N-0.5)**2/S**2) * \
                np.exp(-0.5*(j/N-0.5)**2/S**2)
    z[1, 1:-1, 1:-1] = z[0, 1:-1, 1:-1] + 0.5*eta * \
        (z[0, 2:, 1:-1]+z[0, :-2, 1:-1]+z[0, 1:-1, 2:] +
         z[0, 1:-1, :-2]-z[0, 1:-1, 1:-1]*4.)
    z[:, defect] = 0

    for j in range(1, steps-1):  # time
        z[2, 1:-1, 1:-1] = z[1, 1:-1, 1:-1]*2. - z[0, 1:-1, 1:-1] + eta * \
            (z[1, 2:, 1:-1]+z[1, :-2, 1:-1]+z[1, 1:-1, 2:] +
             z[1, 1:-1, :-2]-z[1, 1:-1, 1:-1]*4.)
        z[2, defect] = 0
        z[0, :, :] = z[1, :, :]
        z[1, :, :] = z[2, :, :]
    Z = z[-1, :, :]

    # x = y = np.linspace(0., L, N+1)
    # vx, vy = np.meshgrid(x, y)
    # fig = plt.figure(figsize=(6.4, 6), dpi=80)
    # ax = fig.gca(projection='3d')
    # ax.set_zlim(-1.1, 1.1)
    # global surf
    # surf = ax.plot_surface(vx, vy, z[2], cmap='viridis')

    # def animate(i):
    #     global z, surf
    #     z[2, 1:-1, 1:-1] = z[1, 1:-1, 1:-1]*2. - z[0, 1:-1, 1:-1] + eta * \
    #         (z[1, 2:, 1:-1]+z[1, :-2, 1:-1]+z[1, 1:-1, 2:] +
    #          z[1, 1:-1, :-2]-z[1, 1:-1, 1:-1]*4.)
    #     z[2, defect] = 0
    #     surf.remove()
    #     surf = ax.plot_surface(vx, vy, z[2], cmap='viridis')
    #     z[0, :, :] = z[1, :, :]
    #     z[1, :, :] = z[2, :, :]

    # anim = animation.FuncAnimation(fig, animate, frames=10, interval=40)
    # plt.tight_layout()
    # plt.show()
    #### END YOUR CODE HERE ####
    return Z


print(calc_wave_displacement(+0.1196))

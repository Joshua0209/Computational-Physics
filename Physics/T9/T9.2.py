import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt


def calc_particle_probability(V0):
    P = np.zeros(2)
    ### START YOUR CODE HERE ###
    dt, dx, tf = 0.00025, 0.05, 0.2
    L, k0, alpha, mu, sigma = 10., 20, dt/dx**2, 2., 0.4
    steps, N = int(tf/dt), int(L/dx)

    # fig = plt.figure(figsize=(8, 4), dpi=80)
    # ax = plt.axes(xlim=(0., L), ylim=(0., 2.))
    # ax.set_xlabel('x')
    # ax.set_ylabel('P(x)')
    # curve, = ax.plot([], [], lw=2, color='Red')

    x = np.linspace(0., L, N+1)
    global R, I
    R = np.exp(-0.5*((x-mu)/sigma)**2) * np.cos(k0*x)  # at half-integer t
    I = np.exp(-0.5*((x-mu)/sigma)**2) * np.sin(k0*x)  # at integer t
    V = np.zeros_like(x)
    V[(N+1)//2:] = V0

    for i in range(steps):
        R[1:-1] = R[1:-1]-alpha * \
            (I[2:]+I[:-2]-2.*I[1:-1])+dt*V[1:-1]*I[1:-1]
        I[1:-1] = I[1:-1]+alpha * \
            (R[2:]+R[:-2]-2.*R[1:-1])-dt*V[1:-1]*R[1:-1]
    p = R**2 + I**2
    ptmp = (p[1:] + p[:-1])/2*dx
    P = np.array([ptmp[:int(len(ptmp)/2)].sum(),
                 ptmp[int(len(ptmp)/2):].sum()])
    P /= P.sum()
    # ax.plot(x, V, lw=2, color='Gray')

    # def animate(i):
    #     global R, I
    #     for i in range(50):
    #         R[1:-1] = R[1:-1]-alpha * \
    #             (I[2:]+I[:-2]-2.*I[1:-1])+dt*V[1:-1]*I[1:-1]
    #         I[1:-1] = I[1:-1]+alpha * \
    #             (R[2:]+R[:-2]-2.*R[1:-1])-dt*V[1:-1]*R[1:-1]
    #     curve.set_data(x, (R**2+I**2))
    #     return curve

    # anim = animation.FuncAnimation(fig, animate, frames=10, interval=40)
    # plt.show()

    #### END YOUR CODE HERE ####
    return P


print(calc_particle_probability(400))

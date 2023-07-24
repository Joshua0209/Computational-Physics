import matplotlib.pyplot as plt
import numpy as np


def calc_phasespace_orbits():
    result = np.zeros(1600)

    ### START YOUR CODE HERE ###
    m, g, L = 1., 9.8, 1.
    t, h = 0., 0.005
    y = np.array([np.pi*0.5, np.pi*0.5, 0., 0.])

    def f(t, y):  # y = [theta1, theta2 , thetap1, thetap2]
        theta1, theta2, thetap1, thetap2 = y
        delta = theta2 - theta1
        thetapp1 = (L*thetap1**2*np.sin(delta)*np.cos(delta) + g*np.sin(theta2)*np.cos(delta)
                    + L*thetap2**2*np.sin(delta) - 2*g*np.sin(theta1))/(2*L-L*np.cos(delta)**2)
        thetapp2 = (-L*thetap2**2*np.sin(delta)*np.cos(delta) + 2*g*np.sin(theta1)*np.cos(delta)
                    - 2*L*thetap1**2*np.sin(delta) - 2*g*np.sin(theta2))/(2*L-L*np.cos(delta)**2)
        return np.array([thetap1, thetap2, thetapp1, thetapp2])

    vx, vy, vt = [], [], []
    while t < 40:
        for step in range(10):
            k1 = f(t, y)
            k2 = f(t+0.5*h, y+0.5*h*k1)
            k3 = f(t+0.5*h, y+0.5*h*k2)
            k4 = f(t+h, y+h*k3)
            y += h/6.*(k1+2.*k2+2.*k3+k4)
            t += h

        vx.append(y[0])
        vy.append(y[2])
        vt.append(t)

    result = np.array([vx, vy]).reshape(-1)
    # fig = plt.figure(figsize=(6, 9), dpi=80)
    # plt.subplot(3, 1, 1)
    # plt.plot(vx, vy)
    # plt.subplot(3, 1, 2)
    # plt.plot(vt, vx)
    # plt.subplot(3, 1, 3)
    # plt.plot(vt, vy)
    # plt.show()
    #### END YOUR CODE HERE ####
    return result

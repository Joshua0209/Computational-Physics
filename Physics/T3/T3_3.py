import numpy as np
import scipy


def double_pendulum_fft(A1, A2):
    result = np.zeros(2)
    ### START YOUR CODE HERE ###
    L, g = 1., 9.8
    t, h = 0., 0.005
    y = np.array([A1, A2, 0., 0.])
    rec = []

    def f(t, y):  # y = [theta1, theta2 , thetap1, thetap2]
        theta1, theta2, thetap1, thetap2 = y
        delta = theta2 - theta1
        thetapp1 = (L*thetap1**2*np.sin(delta)*np.cos(delta) + g*np.sin(theta2)*np.cos(delta)
                    + L*thetap2**2*np.sin(delta) - 2*g*np.sin(theta1))/(2*L-L*np.cos(delta)**2)
        thetapp2 = (-L*thetap2**2*np.sin(delta)*np.cos(delta) + 2*g*np.sin(theta1)*np.cos(delta)
                    - 2*L*thetap1**2*np.sin(delta) - 2*g*np.sin(theta2))/(2*L-L*np.cos(delta)**2)
        return np.array([thetap1, thetap2, thetapp1, thetapp2])

    while t < 20:
        k1 = f(t, y)
        k2 = f(t+0.5*h, y+0.5*h*k1)
        k3 = f(t+0.5*h, y+0.5*h*k2)
        k4 = f(t+h, y+h*k3)
        y += h/6.*(k1+2.*k2+2.*k3+k4)
        t += h

        rec.append(y[1])
    print(len(rec))
    rec = scipy.fft.fft(rec)
    max_mag = 0.
    max_freq = 0.
    N = 4000
    for i in range(N//2):
        mag = abs(rec[i])
        freq = i/N/h
        if mag > max_mag:
            max_mag = mag
            max_freq = freq

    result[0] = max_freq
    result[1] = max_mag

    #### END YOUR CODE HERE ####
    return result


print(double_pendulum_fft(0.1, 0.1))

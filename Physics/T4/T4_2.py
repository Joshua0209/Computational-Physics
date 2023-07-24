import numpy as np


def muon_passing_rate(P):
    result = 0.
    ### START YOUR CODE HERE ###

    M = 105.658          # muon mass in MeV/c^2
    E = (P**2+M**2)**0.5  # muon energy in MeV
    beta = P/E           # muon beta factor
    X0 = 1.436           # copper rad. length in cm (or 12.86 gcm^-2)
    dx = 0.1             # stepping distance in cm
    theta0 = 13.6/beta/P*(dx/X0)**0.5*(1.+0.038*np.log(dx/X0/beta**2))
    for i in range(1000):
        x, y, theta = -10., 0., 0.
        while -10 <= x <= 10:
            rn = np.random.randn(2)
            yp = rn[0]*dx*theta0/(12.)**0.5 + rn[1]*dx*theta0/2.
            tp = rn[1]*theta0
            x += (np.cos(theta)*dx - np.sin(theta)*yp)
            y += (np.sin(theta)*dx + np.cos(theta)*yp)
            theta += tp
        if x > 10.:
            result += 1
    result /= 1000
    #### END YOUR CODE HERE ####
    return float(result)


print(muon_passing_rate(90))

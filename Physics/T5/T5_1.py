import numpy as np


def state_energy(S=np.ones(40)):
    E = 0.
    ### START YOUR CODE HERE ###
    J, gBmub = 1, 0.33

    for i in range(len(S)):
        E += -J*S[i-2]*S[i-1] - J/4*S[i-2]*S[i] - gBmub*S[i-2]
    #### END YOUR CODE HERE ####
    return float(E)

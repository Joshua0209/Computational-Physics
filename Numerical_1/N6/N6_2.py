import numpy as np


def central_cell_is_alive(p):
    decision = True
    ### START YOUR CODE HERE ###
    sum = np.sum(p) - p[1, 1]
    if p[1, 1] == 0 and sum != 3:
        decision = False
    elif p[1, 1] == 1:
        if sum < 2 or sum > 3:
            decision = False
    #### END YOUR CODE HERE ####
    return decision

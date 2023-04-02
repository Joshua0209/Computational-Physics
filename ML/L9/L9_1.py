import numpy as np


def string_to_onehot(input):
    output = np.zeros(27)
    if len(input) >= 2:
        output = np.zeros((len(input), 27))
    ### START YOUR CODE HERE ###
    idx_to_alps = dict((chr(i+96), i) for i in range(1, 27))
    idx_to_alps[" "] = 0

    for i in range(len(input)):
        if len(input) >= 2:
            output[i, idx_to_alps[input[i]]] = 1
        else:
            output[idx_to_alps[input]] = 1

    #### END YOUR CODE HERE ####
    return output

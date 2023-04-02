import math


def evaluate_difference(N):
    ret_value = 0.
    ### START YOUR CODE HERE ###
    tmp = 0
    for i in range(N):
        tmp += 1/(i+1)**2
    ret_value = abs(math.sqrt(6*tmp) - math.pi)
    #### END YOUR CODE HERE ####
    return ret_value

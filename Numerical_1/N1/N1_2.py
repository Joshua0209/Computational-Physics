import math


def evaluate_difference(N):
    ret_value = 0.
    ### START YOUR CODE HERE ###
    tmp = 0
    for i in range(N):
        tmp += 1/math.factorial(i)
    ret_value = abs(tmp - math.e)
    #### END YOUR CODE HERE ####
    return ret_value


print(evaluate_difference(3))

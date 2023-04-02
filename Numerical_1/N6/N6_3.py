import numpy as np

pattern = \
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype='int')


def game_of_life(n):
    p = pattern.copy()
    ### START YOUR CODE HERE ###

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

    for i in range(n):
        p = np.vstack((np.array([0]*len(p[0])), p, np.array([0]*len(p[0]))))
        p = p.T
        p = np.vstack((np.array([0]*len(p[0])), p, np.array([0]*len(p[0]))))
        p = p.T
        p_new = np.zeros_like(p)
        for i in range(1, len(p_new)-1):
            for j in range(1, len(p_new[0])-1):
                if central_cell_is_alive(p[i-1:i+2, j-1:j+2]):
                    p_new[i, j] = 1
                else:
                    p_new[i, j] = 0
        p_new = p_new[1:-1, 1:-1]
        print(p_new)
        p = p_new.copy()
    #### END YOUR CODE HERE ####
    return p


game_of_life(1)

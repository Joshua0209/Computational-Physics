import numpy as np


def calc_magnetization_2D(T):
    M = 0.
    ### START YOUR CODE HERE ###
    J, gBmub, kB = 1, 0.33, 1

    def state_energy(S=np.ones(40)):
        E = 0.
        ### START YOUR CODE HERE #  ##
        E += -J*np.sum(S[:N-1, :]*S[1:, :]) \
            - J*np.sum(S[:, :N-1]*S[:, 1:]) \
            - J*np.sum(S[1:, :N-1]*S[:N-1, 1:]) \
            - gBmub*np.sum(S)
        E += -J*np.sum(S[N-1, :]*S[0, :]) \
            - J*np.sum(S[:, N-1] * S[:, 0]) \
            - J*np.sum(S[0, :N-1]*S[N-1, 1:]) \
            - J*np.sum(S[1:, N-1]*S[:N-1, 0]) \
            - J*np.sum(S[0, N-1]*S[N-1, 0])
        #### END YOUR CODE HERE ####
        return float(E)

    N = 10
    smp_E, smp_M = [], []
    for trial in range(100):
        Sk = np.ones((N, N))
        Ek = state_energy(Sk)
        for it in range(1000):
            St = Sk.copy()
            St[np.random.randint(N), np.random.randint(N)] *= -1.
            Et = state_energy(St)
            P = np.exp(-(Et-Ek)/kB/T)
            if P >= np.random.rand():
                Sk, Ek = St, Et
        Mk = abs(Sk.sum())
        # smp_E.append(Ek)
        smp_M.append(Mk)
    smp_E, smp_M = np.array(smp_E), np.array(smp_M)
    M = smp_M.mean()
    #### END YOUR CODE HERE ####
    return float(M)


print(calc_magnetization_2D(3.8))

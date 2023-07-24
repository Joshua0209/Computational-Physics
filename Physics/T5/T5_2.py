import numpy as np


def calc_magnetization(T):
    M = 0.
    ### START YOUR CODE HERE ###
    J, gBmub, kB = 1, 0.33, 1

    def state_energy(S=np.ones(40)):
        E = 0.
        ### START YOUR CODE HERE ###
        for i in range(len(S)):
            E += -J*S[i-2]*S[i-1] - J/4*S[i-2]*S[i] - gBmub*S[i-2]
        #### END YOUR CODE HERE ####
        return float(E)

    N = 40
    smp_E, smp_M = [], []
    for trial in range(100):
        Sk = np.ones(N)
        Ek = state_energy(Sk)
        for it in range(400):
            St = Sk.copy()
            St[np.random.randint(N)] *= -1.
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


print(calc_magnetization(3.9))

import numpy as np
import matplotlib.pyplot as plt


def solve_electric_potential(A, B):
    U = np.zeros((41, 41))

    ### START YOUR CODE HERE ###
    N, L, w = 40, 1., 1.8
    U = np.zeros((N+1, N+1))
    U[:, 0] = np.sin(A*np.pi*np.linspace(0, 1, N+1))
    U[:, N] = np.sin(B*np.pi*np.linspace(0, 1, N+1))
    U[0, :] = np.sin(A*np.pi*np.linspace(0, 1, N+1))
    U[N, :] = np.sin(B*np.pi*np.linspace(0, 1, N+1))
    for step in range(1000):
        max_delta = 0.
        for i in range(1, N):
            for j in range(1, N):
                delta = (U[i+1, j]+U[i-1, j]+U[i, j+1]+U[i, j-1])/4. - U[i, j]
                U[i, j] += w*delta
                if abs(delta) > max_delta:
                    max_delta = abs(delta)
        print('Step: %3d, max_delta = %g' % (step, max_delta))
        if max_delta < 1E-4:
            break

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x = y = np.linspace(0., L, N+1)
    vx, vy = np.meshgrid(x, y)
    surf = ax.plot_surface(vx, vy, U, cmap='viridis')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('U')
    plt.show()
    #### END YOUR CODE HERE ####
    return U


print(solve_electric_potential(3, 2))

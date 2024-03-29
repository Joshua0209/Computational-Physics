import numpy as np
import matplotlib.pyplot as plt
A = np.array([[[0.,  0.], [0., 0.16]], [[0.81,  0.06], [-0.02, 0.52]],
              [[0.16, -0.29], [0.16, 0.21]], [[-0.11,  0.27], [0.26, 0.3]]])
B = np.array([[0.,  0.], [0.,  1.28], [0.,  1.75], [0.,  0.52]])
C = np.array([0.01, 0.86, 0.07, 0.06])

A = np.array([[[0.,  0.], [0., 0.23]], [[0.76,  0.05], [-0.04, 0.96]],
              [[0.22, -0.19], [0.28, 0.17]], [[-0.15,  0.17], [0.26, 0.22]]])
B = np.array([[0.,  0.], [0.,  1.65], [0.,  1.65], [0.,  0.35]])
C = np.array([0.02, 0.79, 0.12, 0.07])

A = np.array([[[0.,  0.], [0., 0.19]], [[0.93,  0.04], [-0.05, 0.89]],
              [[0.22, -0.18], [0.24, 0.2]], [[-0.16,  0.29], [0.29, 0.16]]])
B = np.array([[0.,  0.], [0.,  1.8], [0.,  1.49], [0.,  0.44]])
C = np.array([0.01, 0.84, 0.09, 0.06])

A = np.array([[[0.,  0.], [0., 0.16]], [[0.79,  0.05], [-0.04, 0.7]],
              [[0.25, -0.33], [0.17, 0.22]], [[-0.16,  0.21], [0.22, 0.26]]])
B = np.array([[0.,  0.], [0.,  1.29], [0.,  1.67], [0.,  0.4]])
C = np.array([0.01, 0.88, 0.05, 0.06])

A = np.array([[[0.,  0.], [0., 0.2]], [[0.74,  0.05], [-0.04, 0.74]],
              [[0.15, -0.3], [0.17, 0.24]], [[-0.14,  0.29], [0.24, 0.31]]])
B = np.array([[0.,  0.], [0.,  1.47], [0.,  1.78], [0.,  0.49]])
C = np.array([0.01, 0.86, 0.06, 0.07])
ntrials = 100000
pos = np.zeros((ntrials, 2))
for n in range(1, ntrials):
    type = np.random.choice(range(4), p=C)
    pos[n] = A[type].dot(pos[n-1])+B[type]
plt.figure(figsize=(12, 8), dpi=80)
plt.scatter(pos[:, 1], pos[:, 0], c=(pos[:, 0]+pos[:, 1])
            * 0.5, alpha=0.5, s=10, marker='.')
plt.show()

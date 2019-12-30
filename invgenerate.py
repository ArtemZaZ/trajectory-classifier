""" Не валидный скрипт, отброшенный в работе"""
import random
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import matplotlib.pyplot as plt

dt = np.linspace(0, 1, 1000)
sx = 0.05 * np.sin(dt*2*np.pi)
sy = 0.05 * np.cos(dt*2*np.pi) - 0.05
sz = 0.0 * np.sin(dt*2*np.pi)
s = [sx, sy, sz]


if __name__ == '__main__':
    a = [np.zeros(len(dt)-1), np.zeros(len(dt)-1), np.zeros(len(dt)-1)]
    for j in range(3):
        for i in range(len(dt)-1):
            a[j][i] = (s[j][i+1] - s[j][i]) / ((dt[i+1] - dt[i])**2)

    print(a)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(sx, sy, sz, 'r')

    fig2 = plt.figure()
    aax = fig2.gca(projection='3d')
    aax.plot(*a, 'b')

    plt.show()

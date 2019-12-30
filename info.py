import random
import time
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

X = np.linspace(-5, 5, 1000)
G = np.exp(-((X - 0) / 1) ** 2)
dG2 = np.gradient(np.gradient(G))
fig = plt.figure()
ax = fig.gca()
ax.plot(X, G, 'r', label='$f(t)$')
ax.plot(X, dG2*1000, 'b', label='$K(f(t))*10^{3}$')
ax.legend()
ax.plot([-5, 5], [0, 0], 'k:')
plt.show()

X, Y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 4, 3, 2, 1]
dG2 = np.gradient(np.gradient(Y))
fig = plt.figure()
ax = fig.gca()
ax.plot(X, Y, 'r', label='$f(t)$')
ax.plot(X, dG2, 'b', label='$K(f(t))$')
ax.legend()
ax.plot([0, 9], [0, 0], 'k:')
plt.show()

from math import *
import random
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import matplotlib.pyplot as plt

dt = np.linspace(0, 1, 1000)
step = dt[1] - dt[0]
ax = 300 * np.sin(dt * 2 * np.pi) #+ 0.01 * random.random())
ay = 300 * np.cos(dt * 2 * np.pi) #+ 0.01 * random.random())
az = 0.0 * np.sin(dt * 2 * np.pi) #+ 0.01 * random.random())

if __name__ == "__main__":
    a = [ax, ay, az]
    fig2 = plt.figure()
    aax = fig2.gca(projection='3d')
    aax.plot(*a, 'b')

    vx0, vy0, vz0 = 0, 0, 0
    sx0, sy0, sz0 = 0, 0, 0

    sx, sy, sz = [], [], []
    sx.append(sx0)
    sy.append(sy0)
    sz.append(sz0)
     
    for i in range(len(dt)):
        vx0, vy0, vz0 = vx0 + ax[i]*step, vy0 + ay[i]*step, vz0 + az[i]*step
        sx0, sy0, sz0 = sx0 + vx0*step + ax[i]*(step**2)/2,\
                        sy0 + vy0*step + ay[i]*(step**2)/2,\
                        sz0 + vz0*step + az[i]*(step**2)/2
        sx.append(sx0)
        sy.append(sy0)
        sz.append(sz0)
        
    fig = plt.figure()
    a = fig.gca(projection='3d')
    a.plot(sx, sy, sz, 'r')
    plt.show()


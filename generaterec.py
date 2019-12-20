import random
import time
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def rect(a, b, c, d, rand=False):
    dt = np.linspace(0, 1, 250)
    firstEdge = np.array([dt * 0, dt * 0, dt * a])
    secondEdge = np.array([dt * b, dt * 0, dt * 0 + a])
    thirdEdge = np.array([dt * 0 + b, dt * 0, -dt * c + a])
    fourthEdge = np.array([-dt * d + b, dt * 0, dt * 0 + a - c])
    sx, sy, sz = np.concatenate([firstEdge, secondEdge, thirdEdge, fourthEdge], axis=1)
    dt = np.linspace(0, 1, 1000)
    if rand:
        ranScale = 100 * 10
        ranYScale = 0.4
        sxierr, syierr, szierr = [[0], [0], [0]]  # псевдоинтегральные ошибки 2ого интегрирования
        vxierr, vyierr, vzierr = [[0], [0], [0]]  # псевдоинтегральные ошибки 1ого интегрирования
        step = dt[1] - dt[0]
        for i in range(len(dt) - 1):
            axerr, ayerr, azerr = ranScale * (random.random() - 0.5), ranYScale * ranScale * (
                    random.random() - 0.5), ranScale * (random.random() - 0.5)  # ошибки ускорения
            vxie, vyie, vzie = vxierr[i] + axerr * step, vyierr[i] + ayerr * step, vzierr[i] + azerr * step
            sxie, syie, szie = sxierr[i] + vxierr[i] * step + axerr * (step ** 2) / 2, \
                               syierr[i] + vyierr[i] * step + ayerr * (step ** 2) / 2, \
                               szierr[i] + vzierr[i] * step + azerr * (step ** 2) / 2
            vxierr.append(vxie)
            vyierr.append(vyie)
            vzierr.append(vzie)
            sxierr.append(sxie)
            syierr.append(syie)
            szierr.append(szie)

        sx = sx + np.array(sxierr)
        sy = sy + np.array(syierr)
        sz = sz + np.array(szierr)
    return sx, sy, sz, dt


if __name__ == '__main__':
    sx, sy, sz, dt = rect(15, 20, 10, 20, False)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(sx, sy, sz, 'r')
    sx, sy, sz, dt = rect(15, 20, 10, 20, True)
    ax.plot(sx, sy, sz, 'b')
    plt.show()

    sxFrame, syFrame, szFrame, dtFrame = [], [], [], []
    for i in range(1000):
        a = 10 * random.random() + 10  # диапазон [10, 20]
        b = 10 * random.random() + 10  # диапазон [10, 20]
        c = 10 * random.random() + 10  # диапазон [10, 20]
        d = 10 * random.random() + 10  # диапазон [10, 20]
        sx, sy, sz, dt = rect(a, b, c, d, True)
        sxFrame.append(sx)
        syFrame.append(sy)
        szFrame.append(sz)
        dtFrame.append(dt)
    df = pd.DataFrame({'sx': sxFrame, 'sy': syFrame, 'sz': szFrame, 'dt': dtFrame})
    df.to_pickle("rect.pkl")

    data = pd.read_pickle('rect.pkl')
    data.info()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for i in range(100):
        sx, sy, sz, dt = data['sx'][i], data['sy'][i], data['sz'][i], data['dt'][i]
        color = '#%06x' % random.randint(0, 0xFFFFFF)
        ax.plot(sx, sy, sz, color=color)
    plt.show()

import random
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def logarif(a, b, c, rand=False):
    dt = np.linspace(0, 1, 1000)
    # логарифмическая спираль
    r = np.exp(dt * b) * a
    sx = -r * np.cos(dt * c) + a
    sy = r * np.sin(dt * c)
    sz = 0.0
    if rand:
        ranScale = 4
        ranZScale = 100 * 0.7
        sxierr, syierr, szierr = [[0], [0], [0]]  # псевдоинтегральные ошибки 2ого интегрирования
        vxierr, vyierr, vzierr = [[0], [0], [0]]  # псевдоинтегральные ошибки 1ого интегрирования
        step = dt[1] - dt[0]
        for i in range(len(dt) - 1):
            axerr, ayerr, azerr = ranScale * (random.random() - 0.5), ranScale * (
                        random.random() - 0.5), ranScale * ranZScale * (random.random() - 0.5)  # ошибки ускорения
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
    """
    sx, sy, sz, dt = logarif(5, 1, 2 * np.pi, False)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(sx, sy, sz, 'r')
    sx, sy, sz, dt = logarif(5, 1, 2 * np.pi, True)
    ax.plot(sx, sy, sz, 'b')
    plt.show()
    """
    sxFrame, syFrame, szFrame, dtFrame = [], [], [], []
    for i in range(1000):
        r = 5 * random.random() + 5  # диапазон [5, 10]
        sx, sy, sz, dt = logarif(r, 1, 2 * np.pi, True)
        sxFrame.append(sx)
        syFrame.append(sy)
        szFrame.append(sz)
        dtFrame.append(dt)
    df = pd.DataFrame({'sx': sxFrame, 'sy': syFrame, 'sz': szFrame, 'dt': dtFrame})
    df.to_pickle("logarifm.pkl")

    data = pd.read_pickle('logarifm.pkl')
    data.info()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for i in range(100):
        sx, sy, sz, dt = data['sx'][i], data['sy'][i], data['sz'][i], data['dt'][i]
        color = '#%06x' % random.randint(0, 0xFFFFFF)
        ax.plot(sx, sy, sz, color=color)
    plt.show()

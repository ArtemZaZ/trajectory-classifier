import random
import time
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def triangle(a, b, c, rand=False):
    """ Генерирует псевдотреугольник, первая точка в (0, 0, 0)
     :param tuple a: Координаты 2й точки псевдотреугольника
     :param tuple b: Координаты 3й точки псевдотреугольника
     :param tuple c: Координаты 4й точки псевдотреугольника
     :param bool rand: Если выставлен этот флаг, то к оригинальному псевдотреугольника будет
      добавлена интегральная ошибка"""
    firstEdge = np.array([np.linspace(0, a[0], 334), np.linspace(0, a[1], 334), np.linspace(0, a[2], 334)])
    secondEdge = np.array([np.linspace(a[0], b[0], 333), np.linspace(a[1], b[1], 333), np.linspace(a[2], b[2], 333)])
    thirdEdge = np.array([np.linspace(b[0], c[0], 333), np.linspace(b[1], c[1], 333), np.linspace(b[2], c[2], 333)])
    sx, sy, sz = np.concatenate([firstEdge, secondEdge, thirdEdge], axis=1)
    dt = np.linspace(0, 1, 1000)    # время параметризовано и представляет собой 333*3+1=1000 точек измерений
    if rand:
        ranScale = 100 * 5  # настраиваемый параметр, который увеличивает значение ошибки по всем осям
        ranYScale = 0.4  # дополнительный параметр, который увеличивает значение ошибки по оси Y
        sxierr, syierr, szierr = [[0], [0], [0]]  # псевдоинтегральные ошибки 2ого интегрирования
        vxierr, vyierr, vzierr = [[0], [0], [0]]  # псевдоинтегральные ошибки 1ого интегрирования
        step = dt[1] - dt[0]    # диапазон времени между измерениями
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
    """
    # Тестирование генератора
    sx, sy, sz, dt = triangle((10, 0, 10), (20, 0, -2), (4, 0, 0), False)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(sx, sy, sz, 'r')
    sx, sy, sz, dt = triangle((10, 0, 10), (20, 0, -2), (4, 0, 0), True)
    ax.plot(sx, sy, sz, 'b')
    plt.show()
    """

    # Генерация 1000 псевдотреугольников с различными параметрами
    sxFrame, syFrame, szFrame, dtFrame = [], [], [], []
    for i in range(1000):
        a = (5 * random.random() + 10, 0, 5 * random.random() + 10)  # рандомайзер параметра ([10, 15], 0, [10, 15])
        b = (5 * random.random() + 15, 0, 6 * random.random() - 3)  # рандомайзер параметра ([15, 20], 0, [-3, 3])
        c = (10 * random.random() - 5, 0, 6 * random.random() - 3)  # рандомайзер параметра ([-5, 5], 0, [-3, 3])
        sx, sy, sz, dt = triangle(a, b, c, True)
        sxFrame.append(sx)
        syFrame.append(sy)
        szFrame.append(sz)
        dtFrame.append(dt)
    df = pd.DataFrame({'sx': sxFrame, 'sy': syFrame, 'sz': szFrame, 'dt': dtFrame})
    df.to_pickle("datasets/triangle.pkl")   # Сохраняем в предварительную БД. Далее она будет обработана в
    # preparedatabase.py

    """
    # Проверка валидности БД
    data = pd.read_pickle("datasets/triangle.pkl")
    data.info()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for i in range(100):
        sx, sy, sz, dt = data['sx'][i], data['sy'][i], data['sz'][i], data['dt'][i]
        color = '#%06x' % random.randint(0, 0xFFFFFF)
        ax.plot(sx, sy, sz, color=color)
    plt.show()
    """
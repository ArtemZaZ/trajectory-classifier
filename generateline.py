import random
import time
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def line(d, rand=False):
    """ генерирует прямую линию
    :param int d: Длина линии
    :param bool rand: Если выставлен этот флаг, то к оригинальной линии будет
     добавлена интегральная ошибка"""
    dt = np.linspace(0, 1, 1000)  # время параметризовано и представляет собой 1000 точек измерений
    sx, sy, sz = dt * d, dt * 0, dt * 0  # описание линии
    if rand:
        ranScale = 100  # настраиваемый параметр, который увеличивает значение ошибки по всем осям
        ranYScale = 2   # дополнительный параметр, который увеличивает значение ошибки по оси Y
        ranZScale = 2   # дополнительный параметр, который увеличивает значение ошибки по оси Z
        sxierr, syierr, szierr = [[0], [0], [0]]  # псевдоинтегральные ошибки 2ого интегрирования
        vxierr, vyierr, vzierr = [[0], [0], [0]]  # псевдоинтегральные ошибки 1ого интегрирования
        step = dt[1] - dt[0]    # диапазон времени между измерениями
        for i in range(len(dt) - 1):
            axerr, ayerr, azerr = ranScale * (random.random() - 0.5), ranYScale * ranScale * (
                    random.random() - 0.5), ranZScale * ranScale * (random.random() - 0.5)  # ошибки ускорения
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
    sx, sy, sz, dt = line(20, False)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(sx, sy, sz, 'r')
    sx, sy, sz, dt = line(20, True)
    ax.plot(sx, sy, sz, 'b')
    plt.show()
    """
    # Генерация 1000 линий с различными параметрами
    sxFrame, syFrame, szFrame, dtFrame = [], [], [], []
    for i in range(1000):
        a = 10 * random.random() + 15  # рандомайзер параметра с диапазоном [15, 25]
        sx, sy, sz, dt = line(a, True)
        sxFrame.append(sx)
        syFrame.append(sy)
        szFrame.append(sz)
        dtFrame.append(dt)
    df = pd.DataFrame({'sx': sxFrame, 'sy': syFrame, 'sz': szFrame, 'dt': dtFrame})
    df.to_pickle("datasets/line.pkl")   # Сохраняем в предварительную БД. Далее она будет обработана в
    # preparedatabase.py

    """
    # Проверка валидности БД
    data = pd.read_pickle('datasets/line.pkl')
    data.info()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for i in range(100):
        sx, sy, sz, dt = data['sx'][i], data['sy'][i], data['sz'][i], data['dt'][i]
        color = '#%06x' % random.randint(0, 0xFFFFFF)
        ax.plot(sx, sy, sz, color=color)
    plt.show()
    """


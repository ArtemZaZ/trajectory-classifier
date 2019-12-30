import random
import time
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def rect(a, b, c, d, rand=False):
    """ Генерирует псевдопрямоугольник
     :param int a: Длина первого ребра псевдопрямоугольника
     :param int b: Длина второго ребра псевдопрямоугольника
     :param int c: Длина третьего ребра псевдопрямоугольника
     :param int d: Длина четвертого ребра псевдопрямоугольника
     :param bool rand: Если выставлен этот флаг, то к оригинальному псевдопрямоугольнику будет
      добавлена интегральная ошибка"""
    dt = np.linspace(0, 1, 250)  # время параметризовано и представляет собой 250*4=1000 точек измерений
    firstEdge = np.array([dt * 0, dt * 0, dt * a])  # описание псевдопрямоугольника
    secondEdge = np.array([dt * b, dt * 0, dt * 0 + a])
    thirdEdge = np.array([dt * 0 + b, dt * 0, -dt * c + a])
    fourthEdge = np.array([-dt * d + b, dt * 0, dt * 0 + a - c])
    sx, sy, sz = np.concatenate([firstEdge, secondEdge, thirdEdge, fourthEdge], axis=1)
    dt = np.linspace(0, 1, 1000)
    if rand:
        ranScale = 100 * 10  # настраиваемый параметр, который увеличивает значение ошибки по всем осям
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
    sx, sy, sz, dt = rect(15, 20, 10, 14, False)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(sx, sy, sz, 'r')
    sx, sy, sz, dt = rect(15, 20, 10, 14, True)
    ax.plot(sx, sy, sz, 'b')
    plt.show()
    """
    # Генерация 1000 псевдопрямоугольников с различными параметрами
    sxFrame, syFrame, szFrame, dtFrame = [], [], [], []
    for i in range(1000):
        a = 10 * random.random() + 10  # рандомайзер параметра с диапазоном [10, 20]
        b = 10 * random.random() + 10  # рандомайзер параметра с диапазоном [10, 20]
        c = 10 * random.random() + 10  # рандомайзер параметра с диапазоном [10, 20]
        d = 10 * random.random() + 10  # рандомайзер параметра с диапазоном [10, 20]
        sx, sy, sz, dt = rect(a, b, c, d, True)
        sxFrame.append(sx)
        syFrame.append(sy)
        szFrame.append(sz)
        dtFrame.append(dt)
    df = pd.DataFrame({'sx': sxFrame, 'sy': syFrame, 'sz': szFrame, 'dt': dtFrame})
    df.to_pickle("datasets/rect.pkl")   # Сохраняем в предварительную БД. Далее она будет обработана в
    # preparedatabase.py
    """
    # Проверка валидности БД
    data = pd.read_pickle("datasets/rect.pkl")
    data.info()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for i in range(100):
        sx, sy, sz, dt = data['sx'][i], data['sy'][i], data['sz'][i], data['dt'][i]
        color = '#%06x' % random.randint(0, 0xFFFFFF)
        ax.plot(sx, sy, sz, color=color)
    plt.show()
    """

import random
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import mode

PATH = 'logarifm.pkl'
PART = 10  # количество частей, на которые делятся перемещения

data = pd.read_pickle(PATH)
data.info()
fig = plt.figure()
ax = fig.gca(projection='3d')
for i in range(100):
    sx, sy, sz, dt = data['sx'][i], data['sy'][i], data['sz'][i], data['dt'][i]
    color = '#%06x' % random.randint(0, 0xFFFFFF)
    ax.plot(sx, sy, sz, color=color)
plt.show()

print(data.shape[0])

keys = []
for i in range(PART):
    keys.append("modeSx" + str(i))
    keys.append("modeSy" + str(i))
    keys.append("modeSz" + str(i))
    keys.append("maxabsSx" + str(i))
    keys.append("maxabsSy" + str(i))
    keys.append("maxabsSz" + str(i))

attributes = dict.fromkeys(keys)
for key in attributes.keys():
    attributes[key] = []

print(attributes)

for i in range(data.shape[0]):
    scale = 1000  # увеличиваем масштаб ф-ии кривизны, чтобы удобнее с ней было работать
    d2sx_dt = np.gradient(np.gradient(data['sx'][i])) * scale  # кривая кривизны для параметра sx
    d2sy_dt = np.gradient(np.gradient(data['sy'][i])) * scale  # кривая кривизны для параметра sy
    d2sz_dt = np.gradient(np.gradient(data['sz'][i])) * scale  # кривая кривизны для параметра sz

    for j in range(PART):
        thisSliceInd = data.shape[0] * j // PART
        d2sx_dt_sl = d2sx_dt[thisSliceInd:thisSliceInd + data.shape[0] // PART]
        d2sy_dt_sl = d2sy_dt[thisSliceInd:thisSliceInd + data.shape[0] // PART]
        d2sz_dt_sl = d2sz_dt[thisSliceInd:thisSliceInd + data.shape[0] // PART]
        d2sx_dt_sl_mode, _ = mode(d2sx_dt_sl)  # мода ф-ии кривизны
        d2sy_dt_sl_mode, _ = mode(d2sy_dt_sl)
        d2sz_dt_sl_mode, _ = mode(d2sy_dt_sl)
        d2sx_dt_sl_maxabs = abs(max(d2sx_dt_sl.min(), d2sx_dt_sl.max(), key=abs))  # максимальное абсолютное значение
        d2sy_dt_sl_maxabs = abs(max(d2sy_dt_sl.min(), d2sy_dt_sl.max(), key=abs))
        d2sz_dt_sl_maxabs = abs(max(d2sz_dt_sl.min(), d2sz_dt_sl.max(), key=abs))
        attributes["modeSx" + str(j)].append(*d2sx_dt_sl_mode)
        attributes["modeSy" + str(j)].append(*d2sy_dt_sl_mode)
        attributes["modeSz" + str(j)].append(*d2sz_dt_sl_mode)
        attributes["maxabsSx" + str(j)].append(d2sx_dt_sl_maxabs)
        attributes["maxabsSy" + str(j)].append(d2sy_dt_sl_maxabs)
        attributes["maxabsSz" + str(j)].append(d2sz_dt_sl_maxabs)

for key in attributes.keys():
    print(len(data['sx']), len(attributes[key]))
    data[key] = attributes[key]

data.info()
data.to_pickle("done_" + PATH)
data.hist(figsize=(16, 8))
plt.show()

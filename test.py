import random
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import mode

data = pd.read_pickle('datasets/v.pkl')
data.info()
fig = plt.figure()
ax = fig.gca(projection='3d')
for i in range(100):
    sx, sy, sz, dt = data['sx'][i], data['sy'][i], data['sz'][i], data['dt'][i]
    color = '#%06x' % random.randint(0, 0xFFFFFF)
    ax.plot(sx, sy, sz, color=color)
plt.show()

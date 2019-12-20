import random
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import mode

PATH = 'done_logarifm.pkl'

data = pd.read_pickle(PATH)
data.info()
data.hist()
plt.show()

import numpy as np
import pandas as pd
from sklearn import neighbors
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

data = pd.read_pickle('done_logarifm.pkl')
rec = pd.read_pickle('done_rect.pkl')
line = pd.read_pickle('done_line.pkl')

data['type'] = [0]*1000
rec['type'] = [1]*1000
line['type'] = [2]*1000

data = data.append(rec)
data = data.append(line)

data.info()
#data.hist()
#plt.show()

attributes = data.drop(['sx', 'sy', 'sz', 'type', 'dt'], axis=1)
moveType = data['type']
xtrain, xtest, ytrain, ytest = train_test_split(attributes, moveType, test_size=0.2, random_state=10)

knn = neighbors.KNeighborsClassifier(n_neighbors=1, metric='euclidean', weights='distance')
knn.fit(xtrain, ytrain)
ytestpredict = knn.predict(xtest)

print("test error: ", np.mean(ytest != ytestpredict)*100)
test = data[data['type'] == 0]
test = test.drop(['sx', 'sy', 'sz', 'type', 'dt'], axis=1)
print(np.sum(knn.predict(test))/1000)

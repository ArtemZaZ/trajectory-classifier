import numpy as np
import pandas as pd
from sklearn import neighbors
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

data = pd.read_pickle('datasets/done_logarifm.pkl')
rec = pd.read_pickle('datasets/done_rect.pkl')
line = pd.read_pickle('datasets/done_line.pkl')
triangle = pd.read_pickle('datasets/done_triangle.pkl')
v = pd.read_pickle('datasets/done_v.pkl')


data['type'] = [0]*1000
rec['type'] = [1]*1000
line['type'] = [2]*1000
triangle['type'] = [3]*1000
v['type'] = [4]*1000

data = data.append(rec)
data = data.append(line)
data = data.append(triangle)
data = data.append(v)


data.info()
#data.hist()
#plt.show()

attributes = data.drop(['sx', 'sy', 'sz', 'type', 'dt'], axis=1)
moveType = data['type']
xtrain, xtest, ytrain, ytest = train_test_split(attributes, moveType, test_size=0.2, random_state=10)

knn = neighbors.KNeighborsClassifier(n_neighbors=1, metric='euclidean', weights='distance')
knn.fit(xtrain, ytrain)
ytestpredict = knn.predict(xtest)
ytrainpredict = knn.predict(xtrain)

print("KNeighborsClassifier test error: ", np.mean(ytest != ytestpredict)*100)
print("KNeighborsClassifier train error: ", np.mean(ytrain != ytrainpredict)*100)


tr = DecisionTreeClassifier(criterion='entropy', max_depth=6, random_state=20, presort=True)
tr.fit(X=xtrain, y=ytrain)
ytestpredict = tr.predict(xtest)
ytrainpredict = tr.predict(xtrain)


print("DecisionTreeClassifier test error: ", np.mean(ytest != ytestpredict)*100)
print("DecisionTreeClassifier train error: ", np.mean(ytrain != ytrainpredict)*100)

tree.export_graphviz(tr, out_file='doc/tree.dot', feature_names=attributes.keys(), class_names=['log', 'rec', 'line', 'triangle', 'v'])


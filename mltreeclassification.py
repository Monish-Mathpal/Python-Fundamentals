dentifying iris flower from set of iris flowers images
import numpy as np
from sklearn.datasets import load_iris
from sklearn import tree
iris = load_iris()

#declaring subarray which is to be deleted
test_idx = [0,50,100]


#np.delete deletes three lines and keeping rest of the data for trainning
train_target = np.delete(iris.target,test_idx)

#axis defines along which data needs to be deleted, test_idx defines which elements or 
#which row needs to be deleted
#deleting the data, going to be used for test_data jus to isolate 
#so that prediction can be tested by using train_data on test_data
train_data = np.delete(iris.data,test_idx,axis=0)

test_target = iris.target[test_idx]

#pulling those three rows deleted from training dataset
test_data = iris.data[test_idx]

clf = tree.DecisionTreeClassifier()

#trying to fit or classify data as per target variable "0,1,2"
clf.fit(train_data, train_target)
# visualizing decision tree
'''
from sklearn.externals.six import StringIO
import pydot 
import pydotplus as pdp
dot_data = tree.export_graphviz(clf, out_file=None, 
                         feature_names=iris.feature_names,  
                         class_names=iris.target_names,  
                         filled=True, rounded=True,  
                         special_characters=True)  
graph = pdp.graph_from_dot_data(dot_data)  
graph.write_pdf("iris.pdf")
'''
#predicting the data by using tree classification model
print clf.predict(test_data) 

print test_data[1], test_target[1]
print iris.feature_names, iris.target_names


# # (2+3+24-5)
# # 这个小括号里有几个整数？有几个加减符号？

# from scipy.sparse.construct import random
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn import svm
# from sklearn.neural_network import MLPClassifier

# X = [
#     [1,0], [1,1], [1,2], [1,8], [1,9], [2,10],[2,11], [2,21], [2,60], [3,102], [3,220]
# ]
# y = [
#     0,0,0,0,0,1,1,1,1,2,2
# ]

# # neigh = KNeighborsClassifier(n_neighbors=2)
# # neigh.fit(X, y)
# # print(neigh.predict(X))

# clf = svm.SVC(C=1000)
# clf.fit(X, y)
# print(clf.predict(X))

# # clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
# # clf.fit(X, y)
# # print(clf.predict(X))

# import re

# it = re.search(r'.*(什么).*', '我们的校园有什么？')
# print(it)

# a = [0,1,2,3,4,5]
# for i in range(0, 5, 3):
#     print(i)

a,b = None, False
if a != b:
    print('yes')

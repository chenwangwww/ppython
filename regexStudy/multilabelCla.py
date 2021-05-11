# from sklearn import datasets
# from sklearn.datasets import make_multilabel_classification
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn import metrics

# X, Y = make_multilabel_classification(n_samples=10, n_features=5, n_classes=3, n_labels=2)
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
# cls = DecisionTreeClassifier()
# cls.fit(X_train, Y_train)
# Y_pred = cls.predict(X_test)
# Y_prob = cls.predict_proba(X_test)
# print(X)
# print('--------------------')
# print(Y)
# print('--------------------')
# print(Y_pred)
# print('--------------------')
# print(Y_prob)

# -------------------------------------------------------------------

# from sklearn import svm
# X = [[48, 49], [48, 50], [48, 51], [49, 48], [49, 49]]
# Y = [49, 49, 49, 50, 50]
# clf = svm.SVR()
# clf.fit(X, Y)
# print(clf.predict([[49, 50]]))

# -------------------------------------------------------------------

{'0':'水果', '1':'蔬菜'}
{'33529&26524':'苹果', '38738&33756':'青菜'}

[[33529, 26524], [38738, 33756]]
[0, 1]

# -------------------------------------------------------------------

{'0':'红色', '1':'绿色'}
{'33529&26524':'苹果', '38738&33756':'青菜'}
[[33529, 26524], [38738, 33756]]
[0, 1]

# -------------------------------------------------------------------

from sklearn import svm

X = [[33529, 26524], [38738, 33756]]
Y = [0, 1]
clf = svm.SVC()
clf.fit(X, Y)
print(clf.predict(X))

# -------------------------------------------------------------------

# 1.输入标签列表: ['红色', '绿色']
# 2.转换成标签字典: {'0':'红色', '1':'绿色'}
# 3.输入与对应的输出字典: {'苹果':'红色', '青菜':'绿色'}
# 4.转换成输入与输出列表: 
#                         [[33529, 26524], [38738, 33756]]
#                         [0, 1]
# 5.svm分类
# 6.保存模型

# -------------------------------------------------------------------
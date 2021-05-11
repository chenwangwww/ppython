from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
import pickle
import os

def getModel(filePath):
    with open(filePath, 'rb') as f:
        model = pickle.load(f)
        print(model.labels)

def getFileName():
    dirs = os.listdir(r'./regexStudy/models')
    count = len(dirs)
    return r'./regexStudy/models/model' + str(count)


class ModelBuilder:
    def __init__(self, model, labels) -> None:
        self._model = model
        self._labels = labels

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, value):
        self._labels = value


class Trainer:
    def __init__(self):
        pass

    def charsToArr(self, chars):
        res = []
        for char in chars:
            o = ord(char)
            res.append(o)
        return res

    def arrToLabels(self, attributes):
        dic = {}
        res = {}
        arrres = []
        s = set(attributes)
        count = 0
        for attribute in s:
            dic.update({attribute: count})
            count += 1
        items = dic.items()
        for a in attributes:
            for item in items:
                if a == item[0]:
                    res.update({a: item[1]})
                    arrres.append(item[1])
                    break
        # print(res)
        return res, arrres

    def dicToData(self, dic):
        items = dic.items()
        names = list(map(lambda a: a[0], items))
        attributes = list(map(lambda a: a[1], items))
        nameInts = list(map(lambda a: self.charsToArr(a), names))
        labels, labelArr = self.arrToLabels(attributes)
        print(names)
        return nameInts, labels, labelArr

    def svcTraining(self, X, ylabels, y):
        param_grid = {'kernel': ['linear', 'rbf',
                                 'poly', 'sigmoid'], 'C': [1e-1, 1, 10]}
        score = 0
        kernel = ''
        C = 0
        for k in param_grid['kernel']:
            for c in param_grid['C']:
                svc = svm.SVC(kernel=k, C=c)
                svc.fit(X, y)
                s = svc.score(X, y)
                if s > score:
                    score = s
                    kernel = k
                    C = c
        print(score, kernel, C)
        best_svc = svm.SVC(kernel=kernel, C=C)
        model = ModelBuilder(best_svc, ylabels)
        self.saveModel(model)

    def saveModel(self, model):
        with open(getFileName(), 'wb') as f:
            pickle.dump(model, f)

    def svcTrain(self, dic):
        X, ylabels, y = self.dicToData(dic)
        print(ylabels)
        self.svcTraining(X, ylabels, y)


trainer = Trainer()
# trainer.arrToLabels(['红色', '绿色', '红色', '绿色','黄色'])
# trainer.dicToData({'苹果':'红色', '青菜':'绿色'})
# trainer.svcTrain({'苹果':'红色', '青菜':'绿色'})

# -------------------------------------------------------------------
dic = {'苹果': '红色', '青菜': '绿色',
       '西瓜': '绿色', '香蕉': '黄色',
       '黄瓜': '绿色', '番茄': '红色',
       '白菜': '白色', '玉米': '黄色', }
dic2 = {'苹果': '水果', '青菜': '蔬菜',
       '西瓜': '水果', '香蕉': '水果',
       '黄瓜': '水果', '番茄': '蔬菜',
       '白菜': '蔬菜', '玉米': '蔬菜', }
trainer.svcTrain(dic)
trainer.svcTrain(dic2)

# getModel('./regexStudy/models/tt.txt')

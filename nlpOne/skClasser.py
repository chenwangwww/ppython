from sklearn import svm

posDic = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'g': 6,
    'h': 7,
    'i': 8,
    'j': 9,
    'k': 10,
    'm': 11,
    'n': 12,
    'nd': 13,
    'nh': 14,
    'ni': 15,
    'nl': 16,
    'ns': 17,
    'nt': 18,
    'nz': 19,
    'o': 20,
    'p': 21,
    'q': 22,
    'r': 23,
    'u': 24,
    'v': 25,
    'wp': 26,
    'ws': 27,
    'x': 28,
}
best_svc = None
def findBestFit(X, y):
    global best_svc
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
    best_svc.fit(X, y)

# --------------------------------------------------------------------
# 8位，0表示None
['池塘', '上', '的', '小', '桥'], ['n', 'nd', 'u', 'a', 'n'], 
[12, 13, 24, 1, 12, 0, 0, 0]
{'标签': 1}

['房间', '里', '的', '床'], ['n', 'nd', 'u', 'n']
[12, 13, 24, 12, 0, 0, 0, 0]
{'标签': 2}
# --------------------------------------------------------------------

# --------------------------------------------------------------------
{
    1: [(0, 1, '有', 3, 4), (3, 4, '在', 0, 1)],
    2: [(0, 1, '有', 3), (3, '在', 0, 1)]
}
# --------------------------------------------------------------------

# X = [[12, 13, 24, 1, 12, 0, 0, 0], [12, 13, 24, 12, 0, 0, 0, 0]]
# y = [1, 2]
# findBestFit(X, y)
# print(best_svc.predict(X))

# --------------------------------------------------------------------

modes = [
    ['n', 'nd', 'u', 'a', 'n'],
    ['n', 'nd', 'u', 'n'],
]

def segment(asub, alist, wordlist):
    asubStr = '&'.join(asub)
    alistStr = '&'.join(alist)
    count = alistStr.count(asubStr)
    indices = []
    res = []
    startIndex = 0
    for i in range(count):
        index = alistStr.find(asubStr, startIndex)
        listIndex = len(alistStr[:index].split('&')) - 1
        indices.append(listIndex)
        startIndex += len(asubStr)
    for ii in indices:
        res.append(wordlist[ii: ii + len(asub)])
    print(res)

asub = ['n', 'nd', 'u', 'a', 'n']
alist = ['p', 'r', 'v', 'n', 'nd', 'u', 'a', 'n', 'wp', 'd', 'v', 'i', 'u', 'v', 'u', 'r', 'a', 'n', 'wp', 'r', 'v', 'u', 'd', 'a', 'wp', 'd', 'a', 'wp']
wordlist = ['每当', '我', '走过', '池塘', '上', '的', '小', '桥', '，', '都', '会', '不由自主', '地', '看', '着', '那些', '小', '鱼', '，', '它们', '玩', '得', '多么', '开心', '、', '多么', '快乐', '。']
segment(asub, alist, wordlist)  

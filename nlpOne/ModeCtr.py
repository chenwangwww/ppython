import re

class NeuronCrtr(object):
    def __init__(self) -> None:
        pass

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

class ModeCtr(object):
    def __init__(self) -> None:
        self._modes = [
            {'mode': [[r'(.*)', r'(.*)吗$', r'(.*)']], 'res':(self.func1, (0, 1, 2)), 'count': 3},
            {'mode': [[r'(.*)', r'(.*)', r'(.*)什么$']], 'res':(self.func2, (0,1)), 'count': 3},
            {'mode': [[r'(.*)', r'(.*)在', r'(.*)哪里$']], 'res':(self.func2, (0,1)), 'count': 3},
            {'mode': [[r'(.*)', r'是', r'比较(.*)'], [r'.*', r'还是', r'(.*)']], 'res':(self.func4, (0,1,2)), 'count': 3},
            {
                'mode': [[r'(.*)', r'(.*有)$', r'(.*)'], [r'^(那)$', r'(.*)', r'(.*)']],
                'res':(self.func3, [(2, 4, 5), (3, 4, 2), (5, 4, 2), (0, 1, 5)]),
                'count': 6
            },
            {
                'mode': [[r'(.+)', r'.*[^有]$', r'.+'], [r'^$', r'(.*)', r'(.+)']],
                'res':(self.func3, [(0, 1, 2)]),
                'count': 3
            },
            {
                'mode': [[r'(.*)', r'(.*)有(.*)$', r'(.*)']],
                'res':(self.func3, [(0, 1, 3), (0, 2, 3)]),
                'count': 4
            },
            {
                'mode': [[r'(.*)', r'(.*)坐落着$', r'(.*)']],
                'res':(self.func3, [(2, 1)]),
                'count': 3
            },
        ]
        self._dataBase = []

    def func1(self, data):
        r = list(filter(lambda a: data[0] in a[0] and data[1]
                        in a[1] and data[2] in a[2], self._dataBase))
        return len(r) > 0

    def func2(self, data):
        r = list(filter(lambda a: data[0] in a[0]
                        and data[1] in a[1], self._dataBase))
        return r

    def func3(self, data):
        pass

    def func4(self, data):
        res = None
        print(data)
        return res

    def fitMode(self, mode, datas):
        r = []
        for m in mode['mode']:
            for data in datas:
                rr = []
                for i in range(3):
                    ret = re.search(m[i], data[i])
                    if ret is not None:
                        rr.append(ret.groups()[0:])
                if len(rr) == 3:
                    temp = []
                    for v in rr:
                        if type(v) == tuple:
                            temp += list(v)
                        else:
                            temp.append(v)
                    r += temp
        # print(len(r), 3*len(mode['mode']))
        # print('r:', r)
        if len(r) == mode['count']:
            resFunc, resIndices = mode['res']
            if type(resIndices) == tuple:
                iter = map(lambda i: r[i], resIndices)
                return [resFunc, list(iter)]
            else:
                result = []
                for resIndex in resIndices:
                    li = list(map(lambda i: r[i], resIndex))
                    result.append(li)
                # print(result)
                self._dataBase += result

    def validateMode(self, datas):
        # print(datas)
        for mode in self._modes:
            self.fitMode(mode, datas)

    def learn(self, paraList):
        print(paraList)
        for a in paraList:
            self._dataBase += a
            self.validateMode(a)
        print(self._dataBase)

    def question(self, datas):
        print(datas)
        for mode in self._modes:
            res = self.fitMode(mode, datas)
            if res is not None:
                print("res is not None", res)
                print(res[0](res[1]))
                break



modeCtr = ModeCtr()
# modeCtr.validateMode(nlpCtr.abstractSentence('我们的校园有鱼池吗？'))
# modeCtr.validateMode(nlpCtr.abstractSentence('我们的校园有什么？'))
# modeCtr.validateMode(nlpCtr.abstractSentence('在我们的校园里有一处美丽的景色，那就是校园的鱼池。'))


# res = re.search(r'(.*)吗？$', '鱼池美丽吗？')
# print(res.groups())

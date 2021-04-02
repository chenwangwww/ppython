from nlpctrFour import NlpCtr

nlpCtr = NlpCtr()

class Mapper(object):
    def __init__(self):
        self.map = {
            'Quantifiers': [
                ['所有', 'ATT', 'every'],
                ['都', 'ADV', 'every'],
                ['每个', 'ATT', 'every'],
                ['一切', 'ATT', 'every'],
                ['任何', 'ATT', 'every'],
                ['有的', 'ATT', 'some']
            ],
            'Negatives': [
                ['并非', 'ADV', 'not'],
                ['不', 'ADV', 'not'],
                ['不要', 'ADV', 'not']
            ],
            'Conjunctions': [
                ['并且', 'ADV', 'and'],
                ['而', 'ADV', 'and']
            ],
        }
        self.map2 = {
            'Conjunctions': [
                ['xor', [('不', '是', 'ADV'), ('是', None, 'HED'), ('就', '是', 'ADV'), ('是', '是', 'COO')]],
            ],
        }

    def getmap2(self, words, SEG):
        items = self.map2.items()
        for item in items:
            vals = item[1]
            for val in vals: 
                val2 = val[1] 
                le = 0   
                res = []         
                if words is not None:
                    for word in words:
                        a, b = nlpCtr.indexToWord(word['dep'], SEG), nlpCtr.indexToWord(word['gov'], SEG)
                        if (a,b,word['type']) in val2:
                            le += 1
                            if word['type'] == 'ADV':
                                res.append(word['dep'])
                if le == len(val2):
                    temp = []
                    for s in range(len(SEG[0])):
                        if (s+1) not in res:
                            temp.append(SEG[0][s])
                    return ''.join(temp), val[0]
        return None, None

    def getMaps(self, words, SEG):
        res = []
        if words is not None:
            for word in words:
                a = self.getMap(word, SEG)
                if a is not None:
                    res.append(a)
        res = res if len(res) > 0 else None
        return res

    def getMap(self, word, SEG):
        maps = self.map.items()
        for map in maps:
            mapValues = map[1]
            for mapValue in mapValues:
                w = nlpCtr.indexToWord(word['dep'], SEG)
                if w == mapValue[0] and word['type'] == mapValue[1]:
                    return [map[0], mapValue[2], word]
        return None

mapper = Mapper()
# [[('some', 'x'), ...], [('A', 'x'), 'arrow', ('not', 'B', 'x'), ...]]
class PredLogCtr(object):
    def __init__(self):
        pass

    def getquantifiers(self, maps, subjs):
        # print(subjs)
        # print(maps)
        res = []
        if maps is not None:
            for map in maps:
                if map[0] == 'Quantifiers':
                    if map[2]['type'] == 'ADV':
                        for sub in subjs:
                            res.append((map[1], map[2])) 
                    elif map[2]['type'] == 'ATT':
                        li = list(filter(
                            lambda a: a == map[2]['gov'], subjs
                        ))
                        res.append((map[1], map[2]))
        res = res if len(res) > 0 else None
        return res

    def getConjunctions(self, maps):
        res = []
        if maps is not None:
            for map in maps:
                if map[0] == 'Conjunctions':
                    res.append((map[1], map[2]))
        res = res if len(res) > 0 else None
        return res

    def getNegatives(self, maps):
        res = []
        if maps is not None:
            for map in maps:
                if map[0] == 'Negatives':
                    res.append((map[1], map[2]))
        res = res if len(res) > 0 else None
        return res

    def b_not_include(self, word, quantifiers, conjunctions, negatives):
        res = None
        fil = list(filter(lambda a: a is not None, [quantifiers, conjunctions, negatives]))
        alist = []
        for fi in fil:
            alist += fi
        for a in alist:
            if a[1] == word:
                res = True
        # print(alist), print(word)
        return res

    def getSubjsIndices(self, RESNLP):
        subjs = []
        for item in RESNLP:
            su = item['subjs']
            if su is not None:
                for a in su:
                    subjs.append(a['master'])
        subjs = list(set(subjs))
        return subjs

    def getWordsFromPredinfo(self, predInfo):
        res = []
        predRelated,subRelated,obRelated = [],[],[]
        predRelated += predInfo['related']
        for am in predInfo['subjs']:
            ar = am['related']
            if ar is not None:
                subRelated += ar
        for am in predInfo['subjs']:
            ar = am['related']
            if ar is not None:
                obRelated += ar
        res = predRelated + subRelated + obRelated
        res = self.uniqueSort(res)
        return res

    #针对元素是字典的列表，获取元素唯一的列表
    def uniqueSort(self, alist):
        if alist is not None:
            temp = [alist[0]]
            for elem in alist:
                if elem not in temp:
                    temp.append(elem)
            return temp
        return None

    def nlpToPredLog(self, sentence):
        resNlp = nlpCtr.abstractSentence(sentence)
        if resNlp is not None:
            rm, conj = mapper.getmap2(nlpCtr.words, nlpCtr.seg)
            if rm is not None:
                resNlp = nlpCtr.abstractSentence(rm)
            # print(rm)
            # print(quantifiers), print(conjunctions), print(negatives)
            re = []
            for item in resNlp:
                ress = {}
                words = self.getWordsFromPredinfo(item)
                maps = mapper.getMaps(words, nlpCtr.seg)
                subjs = self.getSubjsIndices(resNlp)
                quantifiers = self.getquantifiers(maps, subjs)
                conjunctions = self.getConjunctions(maps)
                negatives = self.getNegatives(maps)
                ress['quantifiers'] = quantifiers
                ress['conjunctions'] = conjunctions
                ress['negatives'] = negatives

                predIndices = [item['pred']]
                related = item['related']
                for r in related:
                    bHas = self.b_not_include(r, quantifiers, conjunctions, negatives)
                    if bHas is None:
                        predIndices.append(r['dep'])
                if predIndices is not None:
                    predIndices.sort()
                    print(predIndices)
                    print([nlpCtr.indexToWord(val, nlpCtr.seg) for val in predIndices])
                    ress['pred'] = predIndices
                sus = item['subjs']
                subPart = []
                if sus is not None:
                    for su in sus:
                        sl = su['related']
                        subjectIndices = [su['master']]
                        if sl is not None:
                            for s in sl:
                                bHas = self.b_not_include(s, quantifiers, conjunctions, negatives)
                                if bHas is None:
                                    subjectIndices.append(s['dep'])
                        if subjectIndices is not None:
                            subjectIndices.sort()
                            print(subjectIndices)
                            print([nlpCtr.indexToWord(val, nlpCtr.seg) for val in subjectIndices])
                            subPart.append(subjectIndices)
                ress['subPart'] = subPart
                ous = item['objs']
                obPart = []
                if ous is not None:
                    for su in ous:
                        sl = su['related']
                        objectIndices = [su['master']]
                        if sl is not None:
                            for s in sl:
                                bHas = self.b_not_include(s, quantifiers, conjunctions, negatives)
                                if bHas is None:
                                    objectIndices.append(s['dep'])
                        if objectIndices is not None:
                            objectIndices.sort()
                            print(objectIndices)
                            print([nlpCtr.indexToWord(val, nlpCtr.seg) for val in objectIndices])
                            obPart.append(objectIndices)
                ress['obPart'] = obPart
                re.append(ress)
            if rm is not None:
                re[1]['conjunctions'] = conj
            print(re)
            return re
            
            

predLogCtr = PredLogCtr()

class PredEnv(object):
    def __init__(self):
        self.table = []

    def push(self, data):
        self.table.append(data)

    def ask(self, ques):
        pass

    def getDataFromSentence(self, sentence):
        info = predLogCtr.nlpToPredLog(sentence)
        if len(info) == 1:
            qua = [(info[0]['quantifiers'][0][0], 'x')]
            neg = info[0]['negatives']
            subj = (info[0]['subPart'], 'x')
            obj = (info[0]['obPart'], 'x')
            conj = 'arrow' if info[0]['conjunctions'] == None else info[0]['conjunctions'][0]
            return [qua, [subj, conj, obj]] if neg == None else [neg, qua, [subj, conj, obj]]

    #全称特指规则
    def USRule(self, source):
        dest = []
        source0 = source[0]
        if source0[0] == ('every', 'x'):
            self.recurToCapital(source[1], dest, 'x', 'x')
        print(source)
        print(dest)
        dest = dest if len(dest) > 0 else None
        return dest 

    #存在特指规则
    def ESRule(self, source):
        dest = []
        source0 = source[0]
        if source0[0] == ('some', 'x'):
            self.recurToCapital(source[1], dest, 'x', 'X')
        print(source)
        print(dest)
        dest = dest if len(dest) > 0 else None
        return dest 

    #存在推广规则
    def EGRule(self, source, upltr, lowltr):
        dest = []
        a = ('some', lowltr)
        

    
    def recurToCapital(self, source, dest, val, replace):
        t = type(source)
        if t == list:
            for a in source:
                subt = type(a)
                if subt == tuple:
                    if  val in a:
                        temp = list(a)
                        temp.remove(val)
                        temp.append(replace)
                        dest.append(tuple(temp))
                elif subt == list:
                    temp = []
                    dest.append(temp)
                    self.recurToCapital(a, temp, val, replace)
                else:
                    dest.append(a)


predEnv = PredEnv()

# [[('every', 5)], [[(1, 2, 3, 5)], 'arrow', (7, ), [(8, )]]] 'and' [[('every', 5)], [[(1, 2, 3, 5)], 'arrow', (7, ), [(8, )]]]
# predLogCtr.nlpToPredLog('学术委员会的每个成员都是博士并且是教授。')
# predLogCtr.nlpToPredLog('小明、小霞，和小刘是三兄弟。')
# predLogCtr.nlpToPredLog('我们不要空话，而要行动。')
# predLogCtr.nlpToPredLog('他因为酒驾被交警拘留了。')
# predLogCtr.nlpToPredLog('不是所有人都是长头发。')
# predLogCtr.nlpToPredLog('并非所有人都是长头发。')
# predLogCtr.nlpToPredLog('所有阔叶植物是落叶植物。')
# predLogCtr.nlpToPredLog('有的水生动物是肺呼吸的')
# predLogCtr.nlpToPredLog('一切自然数有大于它的自然数')
# predLogCtr.nlpToPredLog('每人都有一个父亲')
# predLogCtr.nlpToPredLog('这个房子住着小陈、他的兄弟小张和他们的母亲。')
# predLogCtr.nlpToPredLog('所有自然数都是整数')
# predLogCtr.nlpToPredLog('任何整数不是奇数就是偶数')
# predLogCtr.nlpToPredLog('并非每个自然数都是偶数。')

# [[('every', 'x')], [('自然数', 'x'), 'arrow', ('整数', 'x')]]
# [[('every', 'x')], [('整数', 'x'), 'arrow', [('奇数', 'x'), 'xor', ('偶数', 'x')]]]
# ['not', [('every', 'x')], [('自然数', 'x'), 'arrow', ('偶数', 'x')]]
# =>
# [[('some', 'x')], [('自然数', 'x'), 'and', ('奇数', 'x')]]

# ('自然数', 'x'), 'arrow', ('整数', 'x') == ('not', '自然数', 'x'), 'or', ('整数', 'x')
# ['not', [('every', 'x')], [('自然数', 'x'), 'arrow', ('偶数', 'x')]] == [[('some', 'x')], 'not', [('自然数', 'x'), 'arrow', ('偶数', 'x')]]
# ['not', [('every', 'x')], 'A'] == [[('some', 'x')], 'not', 'A']

# (命题逻辑)
# (蕴含式)
# 化简式:
#     [['A', 'and', 'B']] => [['A']]
#     [['A', 'and', 'B']] => [['B']]
# 附加式:
#     [['A']] => [['A', 'or', 'B']]
#     [['B']] => [['A', 'or', 'B']]

#     ['not', ['A']] => [['A', 'arrow', 'B']]
#     [['B']] => [['A', 'arrow', 'B']]
#     ['not', ['A', 'arrow', 'B']] => [['A']]
#     ['not', ['A', 'arrow', 'B']] => ['not', ['B']]
# 析取三段论:
#     ['not', ['A']]      [['A', 'or', 'B']] => [['B']]
# 假言推论:
#     [['A']]     [['A', 'arrow', 'B']] => [['B']]
# 拒取式:
#     ['not', ['B']]      [['A', 'arrow', 'B']] => ['not', ['A']]
# 假言三段论:
#     [['A', 'arrow', 'B']]     [['B', 'arrow', 'C']] => [['A', 'arrow', 'C']]
# 二难推论:
#     [['A', 'or', 'C']]      [['A', 'arrow', 'C']]       [['B', 'arrow', 'C']] => [['C']]

# [['A', 'arrow', 'B']] => [['C', 'or', 'A'], 'arrow', ['C', 'or', 'B']]
# [['A', 'arrow', 'B']] => [['C', 'and', 'A'], 'arrow', ['C', 'and', 'B']]
# [['A']]     [['B']] => [['A', 'and', 'B']]
# #------------------------------------------------------------------------------------

# [[('every', 'x')], [('自然数', 'x'), 'arrow', ('整数', 'x')]]
# =>    (全称特指规则， 小写的"x"表示是个体域中任一个体)
# [[('自然数', 'x'), 'arrow', ('整数', 'x')]]

# [[('some', 'x')], [('自然数', 'x'), 'and', ('奇数', 'x')]]
# =>      (存在特指规则, 大写的"X"表示是个体域中某一个体)
# [[('自然数', 'X'), 'and', ('奇数', 'X')]]

# (存在推广规则)
# [[('自然数', 'X'), 'and', ('奇数', 'X')]]
# =>
# [[('some', 'x')], [('自然数', 'x'), 'and', ('奇数', 'x')]]

# (全称推广规则)
# [[('自然数', 'x'), 'arrow', ('整数', 'x')]]
# =>
# [[('every', 'x')], [('自然数', 'x'), 'arrow', ('整数', 'x')]]

# print(predEnv.getDataFromSentence('所有自然数都是整数'))

# source = [('整数', 'x'), 'arrow', [('奇数', 'x'), 'xor', ('偶数', 'x')]]
# dest = []
# predEnv.recurToCapital(source, dest, 'x', 'W')
# print(source)
# print(dest)

# predEnv.USRule([[('every', 'x')], [('整数', 'x'), 'arrow', [('奇数', 'x'), 'xor', ('偶数', 'x')]]])
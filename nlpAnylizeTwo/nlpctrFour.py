# 先找寻并列谓词，然后对每个谓词递归搜索其他相关的词，确定每个谓词对应的并列主语和并列宾语。
# masterStru = {'master': 主语或宾语, 'related': [(1, 2, 'ATT'), ...]}
# predStru = {'pred':谓语, 'subjs': [masterStru, ...], 'objs': [masterStru, ...], 'related': [(4, 3, 'RAD'), ...]}
# 并列谓语数组
# [predStru, ...]
# ---------------------------------------------------------------

from ltp import LTP
ltp = LTP()

class NlpCtr(object):
    def __init__(self):
        self.seg = None
        self.words = None

    def trans_result(self, depArr, posArr):
        tempposArr = posArr[0]
        tempdepArr = depArr[0]

        tempArr = []
        for item in tempdepArr:
            dic = {
                'dep': item[0],
                'gov': item[1],
                'type': item[2],
                # 'pos': tempposArr[item[0] - 1]
            }
            tempArr.append(dic)
        return tempArr

    def getHED(self, words):
        root = None
        for word in words:
            if word['gov'] == 0 and word['type'] == 'HED':
                root = word['dep']
        return root

    def getWord(self, words, GOV, wType):
        res = None
        for word in words:
            if word['type'] == wType and word['gov'] == GOV:
                res = word['dep']
        return res

    def getWords(self, words, GOV, wType):
        res = []
        for word in words:
            if word['type'] == wType and word['gov'] == GOV:
                res.append(word['dep'])
        res = res if len(res) > 0 else None
        return res

    def get_not_none(self, alist):
        for a in alist:
            if a is not None:
                return a
        return None

    def indexToWord(self, index, seg):
        res = None
        if index and index <= len(seg[0]):
            res = seg[0][index - 1]
        return res

    def getSubject(self, words, PRED):
        pob = None
        sbv = self.getWord(words, PRED, 'SBV')
        rawPredInfo = []
        self.getRelatedInfo(words, PRED, rawPredInfo)
        if rawPredInfo is not None:
            for info in rawPredInfo:
                if self.indexToWord(info['dep'], self.seg) == '被':
                    pob = self.getWord(words, info['dep'], 'POB')  
                if sbv is None and info['type'] == 'SBV':
                    sbv = info['dep']
        return self.get_not_none([sbv, pob])

    def getSubjects(self, words, HED):
        res = []
        subject = self.getSubject(words, HED)
        if subject is not None:
            res.append(subject)
            coos = self.getWords(words, subject, 'COO')
            if coos is not None:
                res += coos        
        return self.get_not_none([res])

    def getSubjs(self, words, HED):
        res = []
        subjs = self.getSubjects(words, HED)
        if subjs is not None:
            for a in subjs:
                resA = []
                self.getRelatedInfo(words, a, resA)
                resSub = {
                    'master': a, 
                    'related': resA if len(resA) > 0 else None
                }
                res.append(resSub)
        res = res if len(res) > 0 else None
        return res

    def getObjs(self, words, HED):
        res = []
        objs = self.getObjects(words, HED)
        if objs is not None:
            for obj in objs:
                resA = []
                self.getRelatedInfo(words, obj, resA)
                resSub = {
                    'master': obj, 
                    'related': resA if len(resA) > 0 else None
                }
                res.append(resSub)
        res = res if len(res) > 0 else None
        return res

    def getObjects(self, words, HED):
        res = []
        vob = self.getWord(words, HED, 'VOB')
        if vob is not None:
            res.append(vob)
            coos = self.getWords(words, vob, 'COO')
            if coos is not None:
                res += coos
        res = res if len(res) > 0 else None
        fob = self.getWord(words, HED, 'FOB')
        return self.get_not_none([res, [fob]])

    # 获取修饰主语、宾语的信息
    def getRelatedInfo(self, words, GOV, RES):
        for word in words:
            if word['gov'] == GOV \
                and word['type'] != 'COO' \
                and word['type'] != 'WP':
                RES.append(word)
                self.getRelatedInfo(words, word['dep'], RES)

    def getPreds(self, words, HED):
        res = [HED]
        coos = self.getWords(words, HED, 'COO')
        if coos is not None:
            res += coos
        return res
    
    # 获取修饰谓语的信息
    def getPredInfo(self, words, GOV, IGNORES, RES):
        for word in words:
            if word['gov'] == GOV:
                if word['dep'] not in IGNORES \
                    and word['type'] != 'WP' \
                    and word['type'] != 'COO':
                    RES.append(word)
                    self.getPredInfo(words, word['dep'], IGNORES, RES)
        
    
    def abstractSentence(self, sentence):
        res = []
        self.seg, hidden = ltp.seg([sentence])
        dep = ltp.dep(hidden)
        pos = ltp.pos(hidden)
        words = self.trans_result(dep, pos)
        self.words = words
        # print(self.seg)
        # print(dep)

        if len(words) > 0:
            hed = self.getHED(words)
            if hed is not None:
                preds = self.getPreds(words, hed)
                for pred in preds:
                    vob = self.getWord(words, pred, 'VOB')
                    fob = self.getWord(words, pred, 'FOB')
                    object = self.get_not_none([vob, fob])
                    subject = self.getSubject(words, pred)

                    if subject is not None and subject > pred:
                        break

                    ignores = [subject, object]
                    resPred = []
                    self.getPredInfo(words, pred, ignores, resPred)
                    subjs = self.getSubjs(words, pred)
                    objs = self.getObjs(words, pred)
                    predStru = {
                        'pred':pred, 
                        'subjs': subjs, 
                        'objs': objs, 
                        'related': resPred
                    }
                    res.append(predStru)
        
        res = res if len(res) > 0 else None
        if res is not None:
            subjsOne = res[0]['subjs']
            if subjsOne is not None:
                for item in res:
                    if item['subjs'] is None:
                        item['subjs'] = subjsOne

        sou = []
        self.showWords(res, sou)
        # print(sou)
        # print(res)
        return res

    def showWords(self, source, target):
        t = type(source)
        if t == dict:
            items = source.items()
            for item in items:
                subt = type(item[1])
                if subt == list:
                    sub = []
                    target.update({item[0]: sub})
                    self.showWords(item[1], sub)
                elif subt == dict:
                    sub = {}
                    target.update({item[0]: sub})
                    self.showWords(item[1], sub)
                elif subt == int:
                    sub = self.indexToWord(item[1], self.seg)
                    target.update({item[0]: sub})
                else:
                    target.update({item[0]: item[1]})
        elif t == list:
            for a in source:
                subt = type(a)
                if subt == dict:
                    sub = {}
                    target.append(sub)
                    self.showWords(a, sub)

# nlpCtr = NlpCtr()
# res = nlpCtr.abstractSentence('小明、小霞，和小刘是三兄弟。')
# res = nlpCtr.abstractSentence('他因为酒驾被交警拘留了。')
# res = nlpCtr.abstractSentence('学术委员会的每个成员都是博士并且是教授。')
# res = nlpCtr.abstractSentence('我们不要空话，而要行动。')
# res = nlpCtr.abstractSentence('不是所有人都是长头发。')
# res = nlpCtr.abstractSentence('并非所有人都是长头发。')
# res = nlpCtr.abstractSentence('这个房子里住着小陈、他的兄弟小张和他们的母亲。')
# res = nlpCtr.abstractSentence('所有阔叶植物是落叶植物。')        #(∀x)(F(x)→G(x))
# res = nlpCtr.abstractSentence('有的水生动物是肺呼吸的')          #(ヨx)(F(x)∧G(x))
# res = nlpCtr.abstractSentence('一切自然数有大于它的自然数')         #(∀x)(F(x)→(ヨy)(F(y)∧G(x,y)))
# res = nlpCtr.abstractSentence('每人都有一个父亲')                  #(∀x)(F(x)→(ヨy)(F(y)∧G(x,y)))
# res = nlpCtr.abstractSentence('整天不是吃饭就是睡觉,活得真像一头猪。')

# print(res)
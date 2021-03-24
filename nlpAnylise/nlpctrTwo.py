#主语
# 谓语
# 宾语
# 主语的定语数组（定语的状语+介宾关系数组）[attStru, ...]
# 宾语的定语数组（定语的状语+介宾关系数组）
# 谓语的状语数组(状语+介宾关系数组)   [{'adv': 谓语的状语, 'pob': 介宾关系},...]
# 并列谓语数组（并列谓语的宾语、宾语的定语数组、宾语的定语的状语+介宾关系数组）
# [[并列谓语, 宾语, [attStru, ...]], ...]
# 并列主语数组（并列主语的定语数组、定语的状语+介宾关系数组）
# [[并列主语, [attStru, ...]], ...]
# 并列宾语数组（并列宾语的定语数组、定语的状语+介宾关系数组）
# ---------------------------------------------------------------
# attStru = {'attM': 定语, 'adv': 定语的状语, 'pob': 介宾关系, 'att': 定语的定语}
# masterStru = {'master': 主语或宾语, 'rel': [attStru, ...]}
# advStru = {'adv': 状语, 'pob': 介宾关系}
# predStru = {'pred':谓语, 'objs': [masterStru, ...], 'advs': [advStru, ...]}
# 并列主语数组
# [masterStru, ...]
# 并列谓语数组
# [predStru, ...]
# ---------------------------------------------------------------

from ltp import LTP
ltp = LTP()

class NlpCtr(object):
    def __init__(self):
        self.seg = None

    def trans_result(self, depArr):
        tempdepArr = depArr[0]

        tempArr = []
        for item in tempdepArr:
            dic = {
                'dep': item[0],
                'gov': item[1],
                'type': item[2],
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

    def getSubject(self, words, HED, ADVS):
        subject = self.getWord(words, HED, 'SBV')
        if subject is None and ADVS is not None:
            for adv in ADVS:
                if self.indexToWord(adv) == '被':
                    subject = self.getWord(words, adv, 'POB')
        return subject

    def getObject(self, words, HED):
        vob = self.getWord(words, HED, 'VOB')
        fob = self.getWord(words, HED, 'FOB')
        return self.get_not_none([vob, fob])

    # 获取定语相关信息
    def getATTInfo(self, words, GOV):
        atts = self.getWords(words, GOV, 'ATT')
        res = []
        if atts is not None:
            for a in atts:
                adv = self.getWord(words, a, 'ADV')
                pob = self.getWord(words, adv, 'POB')
                res.append((a, (adv, pob)))
        res = res if len(res) > 0 else None
        return res

    # 获取并列主语或宾语的相关信息
    def getCOOInfo(self, words, GOV):
        res = []
        coos = self.getWords(words, GOV, 'COO')
        if coos is not None:
            for coo in coos:
                atts = self.getATTInfo(words, coo)
                res.append((coo, atts))
        res = res if len(res) > 0 else None
        return res

    # 状语+介宾关系数组
    def getADVPOBS(self, words, ADVS):
        res = []
        if ADVS is not None:
            for adv in ADVS:
                pob = self.getWord(words, adv, 'POB')
                res.append((adv, pob))
        res = res if len(res) > 0 else None
        return res

    def get_not_none(self, alist):
        for a in alist:
            if a is not None:
                return a
        return None

    def recuTran(self, source, target):
        t = type(source)
        if t == list or t == tuple:
            for a in source:
                subt = type(a)
                if subt == list or subt == tuple:
                    target.append([])
                    self.recuTran(a, target[-1])
                else:
                    target.append(self.indexToWord(a))

    def indexToWord(self, index):
        res = None
        if index and index <= len(self.seg[0]):
            res = self.seg[0][index - 1]
        return res

    def showWords(self, dic):
        items = dic.items()
        target = {}
        for item in items:
            t = type(item[1])
            if t == list or t == tuple:
                sub = []
                self.recuTran(item[1], sub)
                target.update({item[0]: sub})
            elif item[1] is not None:
                sub = self.indexToWord(item[1])
                target.update({item[0]: sub})
        print(dic)
        print(target)

    def abstractSentence(self, sentence):
        dic = None
        self.seg, hidden = ltp.seg([sentence])
        dep = ltp.dep(hidden)
        pos = ltp.pos(hidden)
        words = self.trans_result(dep)
        if len(words) > 0:
            hed = self.getHED(words)
            if hed is not None:
                coos = self.getWords(words, hed, 'COO')     #并列谓语
                advs = self.getWords(words, hed, 'ADV')     #谓语的状语
                aps = self.getADVPOBS(words, advs)          #谓语的状语+介宾关系
                subject = self.getSubject(words, hed, advs) #主语
                object = self.getObject(words, hed)         #宾语
                attsS = self.getATTInfo(words, subject)     #主语的定语
                attsO = self.getATTInfo(words, object)      #宾语的定语
                coosS = self.getCOOInfo(words, subject)     #并列主语
                coosO = self.getCOOInfo(words, object)      #并列宾语
                dic = {
                    'subject': subject,
                    'object': object,
                    'pred': hed,
                    'coos': coos,
                    'advs': advs,
                    'aps': aps,
                    'attsS': attsS,
                    'attsO': attsO,
                    'coosS': coosS,
                    'coosO': coosO
                }
        self.showWords(dic)
        return dic

nlpCtr = NlpCtr()
# nlpCtr.abstractSentence('他因为酒驾被交警拘留了。')
# nlpCtr.abstractSentence('学术委员会的每个成员都是博士并且是教授。')
nlpCtr.abstractSentence('小明、小霞，和小刘是三兄弟。')
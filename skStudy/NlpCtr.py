from ltp import LTP
ltp = LTP()


class NlpCtr(object):
    def __init__(self):
        self.seg = None
        self.words = None
        self.dep = None

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

    # 获取中心词索引
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

    # 索引转字符串
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

    # 获取修饰主语、宾语的信息
    def getRelatedInfo(self, words, GOV, RES):
        for word in words:
            if word['gov'] == GOV \
                    and word['type'] != 'COO' \
                    and word['type'] != 'WP':
                RES.append(word)
                self.getRelatedInfo(words, word['dep'], RES)

    # 获取修饰主语、宾语的信息（仅索引）
    def getRelatedInfo2(self, words, GOV, RES):
        for word in words:
            if word['gov'] == GOV \
                    and word['type'] != 'COO' \
                    and word['type'] != 'WP':
                RES.append(word['dep'])
                self.getRelatedInfo2(words, word['dep'], RES)

    # 获取所有谓词
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
                if word['dep'] not in IGNORES:
                    if word['type'] != 'WP' and word['type'] != 'COO':
                        RES.append(word['dep'])
                        self.getPredInfo(words, word['dep'], IGNORES, RES)
    
    def abstSentReal(self, sentence):
        self.seg, hidden = ltp.seg([sentence])
        dep = ltp.dep(hidden)
        words = self.trans_result(dep)
        self.words = words
        self.dep = dep

    def abstractSentence(self, sentence):
        res = []
        self.seg, hidden = ltp.seg([sentence])
        dep = ltp.dep(hidden)
        words = self.trans_result(dep)
        self.words = words
        self.dep = dep
        subject = None
        if len(words) > 0:
            hed = self.getHED(words)
            if hed is not None:
                preds = self.getPreds(words, hed)
                for pred in preds:
                    # 添加修饰主语的部分
                    su = self.getSubject(words, pred)
                    if su is not None and subject is None:
                        subject = su
                    su = su if su is not None else subject
                    resSu = []
                    if su:
                        self.getRelatedInfo2(words, su, resSu)
                        resSu += [su]
                    resSu.sort()

                    # 添加修饰宾语的部分
                    vob = self.getWord(words, pred, 'VOB')
                    fob = self.getWord(words, pred, 'FOB')
                    obj = self.get_not_none([vob, fob])
                    resObj = []
                    if obj:
                        self.getRelatedInfo2(words, obj, resObj)
                        resObj += [obj]
                    resObj.sort()
                    
                    # 添加修饰谓语的部分
                    resPred = []
                    self.getPredInfo(words, pred, [su, obj], resPred)
                    resPred += [pred]
                    resPred.sort()
                    
                    subRes = []
                    subRes.append(self.indicesToSent(resSu))
                    subRes.append(self.indicesToSent(resPred))
                    subRes.append(self.indicesToSent(resObj))
                    res.append(subRes)
        res = res if len(res) > 0 else None
        print(res)
        return res

    def indicesToSent(self, indices):
        r = ''
        for i in indices:
            r += self.seg[0][i - 1]
        return r

nlpCtr = NlpCtr()
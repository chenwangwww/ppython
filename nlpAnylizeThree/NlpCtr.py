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
        sbv = self.getWord(words, PRED, 'SBV')       
        return sbv

    def abstractSentence(self, sentence):
        res = []
        self.seg, hidden = ltp.seg([sentence])
        dep = ltp.dep(hidden)
        pos = ltp.pos(hidden)
        words = self.trans_result(dep, pos)
        self.words = words

        if len(words) > 0:
            hed = self.getHED(words)
            if hed is not None:
                vob = self.getWord(words, hed, 'VOB')
                fob = self.getWord(words, hed, 'FOB')
                object = self.get_not_none([vob, fob])
                subject = self.getSubject(words, hed)
                attSubj = self.getWord(words, subject, 'ATT')
                attObj = self.getWord(words, object, 'ATT')
                res = {
                    'pred': self.indexToWord(hed, self.seg), 
                    'subject': self.indexToWord(subject, self.seg), 
                    'object': self.indexToWord(object, self.seg), 
                    'attSubj': self.indexToWord(attSubj, self.seg),
                    'attObj': self.indexToWord(attObj, self.seg),
                }
        print(res)
        return res

nlpCtr = NlpCtr()
# info = nlpCtr.abstractSentence('1是整数')

# from ClsCreater import ClsCreater
# val1 = ClsCreater(info['object'])

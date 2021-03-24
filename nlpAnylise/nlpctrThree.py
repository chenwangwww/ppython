# attStru = {'attM': 定语, 'adv': 定语的状语, 'pob': 介宾关系, 'att': 定语的定语}
# masterStru = {'master': 主语或宾语, 'rel': [attStru, ...]}
# advStru = {'adv': 状语, 'pob': 介宾关系}
# predStru = {'pred':谓语, 'subjs': [masterStru, ...], 'objs': [masterStru, ...], 'advs': [advStru, ...]}
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

    def getWord2(self, words, wType):
        res = None
        for word in words:
            if word['type'] == wType:
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
                if self.indexToWord(adv, self.seg) == '被':
                    subject = self.getWord(words, adv, 'POB')
        if subject is None:
            subject = self.getWord2(words, 'SBV')
        return subject

    def get_not_none(self, alist):
        for a in alist:
            if a is not None:
                return a
        return None

    def getObjects(self, words, HED):
        res = []
        vob = self.getWord(words, HED, 'VOB')
        while vob is not None:
            res.append(vob)
            vob = self.getWord(words, vob, 'VOB')
        res = res if len(res) > 0 else None
        fob = self.getWord(words, HED, 'FOB')
        return self.get_not_none([res, [fob]])

    # 获取定语相关信息
    def getATTInfo(self, words, GOV):
        atts = self.getWords(words, GOV, 'ATT')
        res = []
        if atts is not None:
            for a in atts:
                adv = self.getWord(words, a, 'ADV')
                pob = self.getWord(words, adv, 'POB')
                att2 = self.getWord(words, a, 'ATT')
                attStru = {
                    'attM': a,
                    'adv': adv,
                    'pob': pob,
                    'att': att2,
                }
                res.append(attStru)
        res = res if len(res) > 0 else None
        return res

    # 获取并列主语的相关信息
    def getCOOInfo(self, words, HED, ADVS):
        res = []
        subject = self.getSubject(words, HED, ADVS) #主语
        attsS = self.getATTInfo(words, subject)     #主语的定语
        masterStru = {
            'master': subject,
            'rel': attsS
        }
        res.append(masterStru)
        coos = self.getWords(words, subject, 'COO')
        if coos is not None:
            for coo in coos:
                atts = self.getATTInfo(words, coo)
                masterStru = {
                    'master': coo,
                    'rel': atts
                }
                res.append(masterStru)
        res = res if len(res) > 0 else None
        return res

    # 状语+介宾关系数组
    def getADVPOBS(self, words, ADVS):
        res = []
        if ADVS is not None:
            for adv in ADVS:
                pob = self.getWord(words, adv, 'POB')
                advStru = {'adv': adv, 'pob': pob}
                res.append(advStru)
        res = res if len(res) > 0 else None
        return res

    #获取宾语相关信息数组
    def getObjsInfo(self, words, objs):
        res = []
        if objs is not None:
            for obj in objs:
                atts = self.getATTInfo(words, obj)      #宾语的定语
                stru = {'master': obj, 'rel': atts}
                res.append(stru)
        res = res if len(res) > 0 else None
        return res

    # 并列谓语数组
    def getPREDInfo(self, words, HED, ADVS):
        res = []
        coos = self.getWords(words, HED, 'COO')     #并列谓语
        aps = self.getADVPOBS(words, ADVS)
        objects = self.getObjects(words, HED)         #宾语
        objs = self.getObjsInfo(words, objects)
        predStru = {
            'pred':HED,
            'objs': objs,
            'advs': aps
        }
        res.append(predStru)
        if coos is not None:
            for coo in coos:
                objects2 = self.getObjects(words, coo)         #宾语
                objs2 = self.getObjsInfo(words, objects2)    
                advs = self.getWords(words, coo, 'ADV')  
                aps2 = self.getADVPOBS(words, advs)   
                pre = {
                    'pred':coo,
                    'objs': objs2,
                    'advs': aps2
                }
                res.append(pre)
        res = res if len(res) > 0 else None
        return res

    def adjustSentence(self, sentence):
        dic = {
            'sentence': sentence,
            'condition': None
        }
        seg, hidden = ltp.seg([sentence])
        dep = ltp.dep(hidden)
        pos = ltp.pos(hidden)
        words = self.trans_result(dep)
        if len(words) > 0:
            hed = self.getHED(words)
            if hed is not None:
                advs = self.getWords(words, hed, 'ADV')     
                subj1 = self.getWord(words, hed, 'SBV')
                subj2 = self.getWord2(words, 'SBV')
                if subj1 is None and subj2 is not None:
                    hedW = self.indexToWord(hed, seg)
                    seg[0] = seg[0][:(hed-1)] + seg[0][hed:]
                    word = ''
                    if advs is not None:
                        for a in advs:
                            word += self.indexToWord(a, seg)
                            seg[0] = seg[0][:(a-1)] + seg[0][a:]
                            
                    dic['condition'] = word + hedW
        dic['sentence'] = ''.join(seg[0])
        return dic
        
    
    def abstractSentence(self, rawSentence):
        adjustRes = self.adjustSentence(rawSentence)
        sentence = adjustRes['sentence']
        
        dic = None
        self.seg, hidden = ltp.seg([sentence])
        dep = ltp.dep(hidden)
        pos = ltp.pos(hidden)
        words = self.trans_result(dep)
        if len(words) > 0:
            hed = self.getHED(words)
            if hed is not None:
                advs = self.getWords(words, hed, 'ADV')     #谓语的状语                
                subjs = self.getCOOInfo(words, hed, advs)
                if advs is not None:
                    advs = list(filter(lambda a: self.indexToWord(a, self.seg) != '被', advs))
                preds = self.getPREDInfo(words, hed, advs)
                dic = {
                    'preds': preds,
                    'subjs': subjs,
                }
        sou = {}
        self.showWords(dic, sou)
        sou['condition'] = adjustRes['condition']
        return dic, sou

    def indexToWord(self, index, seg):
        res = None
        if index and index <= len(seg[0]):
            res = seg[0][index - 1]
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
                else:
                    sub = self.indexToWord(item[1], self.seg)
                    target.update({item[0]: sub})
        elif t == list:
            for a in source:
                subt = type(a)
                if subt == dict:
                    sub = {}
                    target.append(sub)
                    self.showWords(a, sub)


class PredLogistics(object):
    def __init__(self):
        pass

    def analysier(self, dic, dicW):
        print(dicW)
        quantifier = self.getQuantifier(dic, dicW)
        preds = self.getPreds(dicW)
        print(quantifier)
        if quantifier and quantifier['quantifier'] == 'every':
            print('arrow')
        print(preds)

    def getATTS(self, rel):
        res = []
        if rel is not None:
            for r in rel:
                item = r['att'] + r['attM'] if r['att'] is not None else r['attM']
                res.append(item)
        res = res if len(res) > 0 else None
        return res

    def getQuantifierKeyword(self, item, condition):
        res = {
            'quantifier': None,
            'att': ''
        }
        if item is not None and item['atts'] is not None:
            for r in item['atts']:
                if r.find('每个') > -1 or r.find('所有') > -1:
                    res['quantifier'] = 'every'
                elif  r.find('有的') > -1:
                    res['quantifier'] = 'some'
                else:
                    res['att'] += r
        res['att'] += item['master']
        if item['master'] is not None and item['atts'] is None:
            res['quantifier'] = 'some'
        if condition == '不是':
            res['cond'] = 'not'
        res = res if res['quantifier'] is not None else None
        return res

    def getQuantifierKeywordMul(self, items):
        res = {
            'quantifier': None,
            'att': []
        }
        if items is not None:
            for item in items:
                res['att'].append(item['master'])
        res['quantifier'] = 'every'
        res = res if res['quantifier'] is not None else None
        return res

    def getPreds(self, dicW):
        res = []
        preds = dicW['preds']
        if preds is not None:
            for pred in preds:
                # item = pred['pred'] + ''.join(a['master'] for a in pred['objs']) if pred['objs'] is not None else pred['pred']
                fil = filter(lambda a: a['adv'].find('并且') > -1, pred['advs']) if pred['advs'] is not None else []
                conj = 'and' if len(list(fil)) > 0 else None
                
                if conj is not None:
                    res.append(conj)
                res.append(pred)
        res = res if len(res) > 0 else None
        return res
    
    def getQuantifier(self, dic, dicW):
        subjs = dicW['subjs']
        res = []
        quantifier = None
        if subjs is not None:
            for subj in subjs:
                master = subj['master']
                rel = subj['rel']
                atts = self.getATTS(rel)
                item = {
                    'master': master,
                    'atts': atts
                }
                res.append(item)
        length = len(res)
        if length == 1:
            quantifier = self.getQuantifierKeyword(res[0], dicW['condition'])
        elif length > 1:
            quantifier = self.getQuantifierKeywordMul(res)
            
        return quantifier

nlpCtr = NlpCtr()
# a, b = nlpCtr.abstractSentence('小明、小霞，和小刘是三兄弟。')
# a, b = nlpCtr.abstractSentence('他因为酒驾被交警拘留了。')
# a, b = nlpCtr.abstractSentence('学术委员会的每个成员都是博士并且是教授。')
a, b = nlpCtr.abstractSentence('我们不要空话，而要行动。')
# a, b = nlpCtr.abstractSentence('不是所有人都是长头发。')
# nlpCtr.abstractSentence('不是所有人都长头发。')
# a, b = nlpCtr.abstractSentence('所有阔叶植物是落叶植物。')        #(∀x)(F(x)→G(x))
# a, b = nlpCtr.abstractSentence('有的水生动物是肺呼吸的')          #(ヨx)(F(x)∧G(x))
# a, b = nlpCtr.abstractSentence('一切自然数有大于它的自然数')         #(∀x)(F(x)→(ヨy)(F(y)∧G(x,y)))
# a, b = nlpCtr.abstractSentence('每人都有一个父亲')                  #(∀x)(F(x)→(ヨy)(F(y)∧G(x,y)))

predLog = PredLogistics()
predLog.analysier(a, b)

# nlpCtr.adjustSentence('不是所有人都是长头发。')

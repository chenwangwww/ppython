# [[('every', 5)], [('自然数', 'x'), 'and', ('奇数', 'x')]]
from ltp import LTP
ltp = LTP()


class NlpCtr(object):
    def __init__(self):
        self.seg = None
        self.words = None
        self.dep = None

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
                        and (word['type'] != 'LAD' and self.indexToWord(word['dep'], self.seg) != '和') \
                        and word['type'] != 'COO':
                    RES.append(word['dep'])
                    self.getPredInfo(words, word['dep'], IGNORES, RES)

    def abstSentReal(self, sentence):
        self.seg, hidden = ltp.seg([sentence])
        dep = ltp.dep(hidden)
        pos = ltp.pos(hidden)
        words = self.trans_result(dep, pos)
        self.words = words
        self.dep = dep

    def abstractSentence(self, sentence):
        res = []
        self.seg, hidden = ltp.seg([sentence])
        dep = ltp.dep(hidden)
        pos = ltp.pos(hidden)
        words = self.trans_result(dep, pos)
        self.words = words
        self.dep = dep
        subject = None
        if len(words) > 0:
            hed = self.getHED(words)
            if hed is not None:
                preds = self.getPreds(words, hed)
                for pred in preds:
                    su = self.getSubject(words, pred)
                    if su is not None:
                        subject = su
                    resPred = []
                    if not su and subject:
                        resPred += [subject]
                    self.getPredInfo(words, pred, [], resPred)
                    resPred += [pred]
                    resPred.sort()
                    r = ''
                    for i in resPred:
                        r += self.seg[0][i - 1]
                    res.append(r)
        res = res if len(res) > 0 else None
        return res


nlpCtr = NlpCtr()


class Conjs(object):
    def __init__(self):
        self.conjs = []

    def push(self, sentence, item):
        res = (sentence.replace(item[0], item[3], 1), item[1], item[2])
        self.conjs.append(res)


class Mapper(object):
    def __init__(self):
        self.conjs = [
            (('不是', '', '', '是'), ('就是', 'xor', '', '是')),
            (('不要', '', 'not', '要'), ('而要', 'and', '', '要')),
            (('都是', '', '', '是'), ('并且是', 'and', '', '是')),
        ]
        self.quas = [
            ['所有', 'ATT', 'every'],
            ['任意', 'ATT', 'every'],
            ['每个', 'ATT', 'every'],
            ['一切', 'ATT', 'every'],
            ['任何', 'ATT', 'every'],
            ['有的', 'ATT', 'some'],
            ['某些', 'ATT', 'some']
        ]
        self.negs = [
            ['并非', 'ADV', 'not', 'qua'],
            ['不', 'ADV', 'not', 'sent'],
            ['不要', 'ADV', 'not', 'sent']
        ]

    def abstConjs(self, sentence):
        print('sentence', sentence)
        res = None
        conjsList = []
        seg, hidden = ltp.seg([sentence])
        pos = ltp.pos(hidden)
        wps = []
        for i in range(len(pos[0])):
            if pos[0][i] == 'wp':
                wps.append(len(''.join(seg[0][:i])))
        for conj in self.conjs:
            length = len(conj)
            count = 0
            indices = []
            cc = []
            for c in conj:
                if c[0] in sentence:
                    count += 1
                    indices.append(sentence.find(c[0]))
                    cc.append(c)
            print('cc', cc)
            if count == length:
                conjs = Conjs()
                if count == 2:
                    ind0 = list(
                        filter(lambda a: a > indices[0] and a < indices[1], wps))
                    ind1 = list(filter(lambda a: a > indices[1], wps))
                    if len(wps) > 0:
                        if len(ind0) > 0:
                            subsent = sentence[indices[0]: ind0[0]]
                            conjs.push(subsent, cc[0])
                        else:
                            subsent = sentence[indices[0]: indices[1]]
                            conjs.push(subsent, cc[0])
                        if len(ind1) > 0:
                            conjs.push(sentence[indices[1]: ind1[0]], cc[1])
                    else:
                        conjs.push(sentence[indices[0]: indices[1]], cc[0])
                        conjs.push(sentence[indices[1]:], cc[1])
                    endindex = ind1[0] if len(ind1) > 0 else None
                    print('ind0. ind1, endindex:', ind0, ind1, endindex)
                    print('conjs.conjs', conjs.conjs)
                    print('indices', indices)
                    res = sentence[: indices[0]] + conjs.conjs[1][0]
                    if endindex is not None:
                        res += sentence[endindex:]
                    conjsList.append(conjs)
                    
        res = {
            'conjsList': conjsList,
            'sentence': res
        } if res else None
        return res

    def abstComplex(self, sentence):
        info = self.abstConjs(sentence)
        if info:
            sents = nlpCtr.abstractSentence(info['sentence'])
            newConjs = Conjs()
            for sent in sents:
                for c in info['conjsList']:
                    conj = c.conjs
                    index = sent.find(conj[1][0])
                    if index > -1:
                        a = sent[:index] + conj[0][0] + \
                            sent[index + len(conj[1][0]):]
                        b = sent
                        newConjs.conjs.append((a, conj[0][1], conj[0][2]))
                        newConjs.conjs.append((b, conj[1][1], conj[1][2]))
                    else:
                        newConjs.conjs.append((sent, 'arrow', ''))
            # print(newConjs.conjs)
            return newConjs
        return None

    def abstNeg(self, sentence):
        res = []
        nlpCtr.abstSentReal(sentence)
        for item in self.negs:
            its = list(filter(lambda a: item[0] == nlpCtr.indexToWord(
                a['dep'], nlpCtr.seg) and item[1] == a['type'] and a['type'] == 'ADV', nlpCtr.words))
            if len(its) > 0:
                for it in its:
                    res.append((it['dep'], item[-1]))
        res = res if len(res) > 0 else None
        return res

    # [[('every', 'x1')], [('整数', 'x1')]      [[('every', 'x2')], [('浮点数', 'x2')]
    def abstQuasReal(self, sentence, replaceChar):
        # print(sentence)
        nlpCtr.abstSentReal(sentence)
        for item in self.quas:
            its = list(filter(lambda a: item[0] == nlpCtr.indexToWord(
                a['dep'], nlpCtr.seg) and item[1] == a['type'] and a['type'] == 'ATT', nlpCtr.words))
            if len(its) > 0:
                it = its[0]
                resPred = []
                nlpCtr.getPredInfo(nlpCtr.words, it['gov'], [], resPred)
                resPred += [it['gov']]
                q = ''
                for j in range(len(nlpCtr.seg[0])):
                    if j+1 not in resPred:
                        q += nlpCtr.seg[0][j]
                    elif j+1 == it['gov']:
                        q += replaceChar

                resPred.remove(it['dep'])
                resPred.sort()

                r = ''
                for i in resPred:
                    if nlpCtr.dep[0][i-1][2] != 'LAD' and nlpCtr.dep[0][i-1][2] != 'RAD':
                        r += nlpCtr.seg[0][i - 1]

                return [(item[2], replaceChar), (r, replaceChar)], q
        return None, None

    def abstQuas(self, sentence):
        sentInfo = []
        resSent = [sentence]
        res = []
        count = 0
        repctr = 'x' + str(count)
        a, b = self.abstQuasReal(sentence, repctr)
        while a is not None:
            sentInfo.append(a)
            count += 1
            repctr = 'x' + str(count)
            resSent[0] = b
            resSent.append(a[1][1])
            a, b = self.abstQuasReal(b, repctr)
        res = [sentInfo, resSent] if len(sentInfo) > 0 else None
        return res

    def abstSent(self, rawSentence):
        infoZ = self.abstQuas(rawSentence)
        sentence = rawSentence
        val0 = []
        val1 = []
        if infoZ is not None:
            sentence = infoZ[1][0]
            sentInfo = infoZ[0]
            length = len(sentInfo)
            for i in range(length):
                val0.append(sentInfo[i][0])
                val1.append(sentInfo[i][1])
                val1.append('and')
            if len(val1) > 0:
                val1.pop()        
        info = self.abstComplex(sentence)
        sents = [(sentence, '', ''), ]
        if info:
            sents = info.conjs
        if len(val0) == 1 and val0[0] == ('some', 'x0'):
            val1.append('and')
        else:
            val1.append('arrow')
        val12 = []
        for sent in sents:
            resSent = []
            resneg = self.abstNeg(sent[0])            
            if resneg is not None:
                resnegIndices = [v[0] for v in resneg]
                q = ''
                for j in range(len(nlpCtr.seg[0])):
                    if j+1 not in resnegIndices:
                        q += nlpCtr.seg[0][j]
                resSent.append(q)
                for i in resneg:
                    if i[1] == 'qua':
                        val0.insert(0, 'not')
                    elif i[1] == 'sent':
                        resSent.insert(0, 'not')
            else:
                resSent.append(sent[0])
            if sent[2] != '':
                resSent.insert(0, sent[2])
            if sent[1] != '':
                val12.append(sent[1])
            val12.append(tuple(resSent))
        val1.append(val12)
        print([val0, val1])
        return [val0, val1]      

m = Mapper()

class PredLogCtr(object):
    def __init__(self):
        pass

    # 所有自然数是整数
    # [[('every', 'x0')], [('自然数', 'x0'), 'arrow', ('x0是整数',)]]
    # =>
    # [('自然数', 'a'), 'arrow', ('a是整数',)]

    # 任何整数不是奇数就是偶数
    # [[('every', 'x0')], [('整数', 'x0'), 'arrow', [('x0是奇数',), 'xor', ('x0是偶数',)]]]
    # =>
    # [('整数', 'A'), 'arrow', [('A是奇数',), 'and', ('not', 'A是偶数')]]
    # =>
    # [('A是奇数',), 'and', ('not', 'A是偶数')]
    # 或者=>
    # [('整数', 'A'), 'arrow', [('not', 'A是奇数'), 'and', ('A是偶数',)]]
    # =>
    # [('not', 'A是奇数'), 'and', ('A是偶数',)]

    # 并非每个自然数是偶数。
    # [['not', ('every', 'x0')], [('自然数', 'x0'), 'arrow', [('x0是偶数。',)]]]
    # =>
    # [[('some', 'x0')], 'not', [('自然数', 'x0'), 'arrow', [('x0是偶数。',)]]]
    # =>
    # ['not', [('自然数', 'A'), 'arrow', [('A是偶数。',)]]]
    # =>
    # ['not', [('not', '自然数', 'A'), 'or', [('A是偶数。',)]]]
    # =>
    # [('自然数', 'A'), 'and', ['not', ('A是偶数。',)]]
    # =>
    # [('自然数', 'A'), 'and', ('not', 'A是偶数。')]

    # 某些自然数是奇数。
    # [[('some', 'x0')], [('自然数', 'x0'), 'and', ('x0是奇数。',)]]
    # =>
    # [('自然数', 'A'), 'and', ('A是奇数。',)]

    def deleteArrow(self, source):
        if len(source) == 3 and source[1] == 'arrow':
            return source[-1]
        else:
            return source

    def deleteMiddleNeg(self, source, dest):
        if source[0] == 'not':
            for a in source[1]:
                t = type(a)
                if t == list:
                    dest.append('not')
                    dest.append(a)
                elif t == tuple:
                    val0 = a[1:] if a[0] == 'not' else tuple(['not'] + list(a[:]))
                    dest.append(val0)
                elif t == str:
                    val1 = 'and' if a == 'or' else 'or'
                    dest.append(val1)

    def arrowToOr(self, source):
        if len(source) == 3 and source[1] == 'arrow':
            val0 = source[0][1:] if source[0][0] == 'not' else tuple(['not'] + list(source[0][:]))
            val1 = 'or'
            val2 = source[2]
            return [val0, val1, val2]
        return None

    # 否定后移
    def negRule(self, source, dest):
        item0 = source[0]
        if item0[0] == 'not':
            de = []
            for a in item0[1:]:
                tt = []
                if a[0] == 'every':
                    tt.append('some')
                else:
                    tt.append('every')
                tt += list(a)[1:]
                de.append(tuple(tt))
            dest.append(de)
            dest.append('not')
        else:
            dest.append(item0)
        dest += source[1:]
        return dest

    # 消除多余的中括号
    def deleteSpareBracket(self, source, dest):
        t = type(source)
        if t == list:
            if len(source) == 1:
                dest.append(source[0])
            else:
                for a in source:
                    subt = type(a)
                    if subt == list:
                        if len(a) == 1:
                            dest.append(a[0])
                        else:
                            temp = []
                            dest.append(temp)
                            self.deleteSpareBracket(a, temp)
                    else:
                        dest.append(a)

    def recurTo(self, source, dest, val, replace):
        t = type(source)
        if t == list:
            for a in source:
                subt = type(a)
                if subt == tuple:
                    if val in a:
                        temp = list(a)
                        temp.remove(val)
                        temp.append(replace)
                        dest.append(tuple(temp))
                    elif val in a[-1]:
                        temp = list(a)
                        temp[-1] = temp[-1].replace(val, replace)
                        dest.append(tuple(temp))
                elif subt == list:
                    temp = []
                    dest.append(temp)
                    self.recurTo(a, temp, val, replace)
                else:
                    dest.append(a)

    def adjustInfo(self, source, dest):
        for a in source:
            t = type(a)
            if t == tuple:
                if (len(a) == 2 and a[0] != 'not') or (len(a) == 3 and a[0] == 'not'):
                    val0 = a[-1] + '是' + a[-2]
                    val = (val0,) if len(a) == 2 else (a[0], val0)
                    dest.append(val)
                else:
                    dest.append(a)
            else:
                dest.append(a)
    
    def predToStatement(self, rawpred):
        pred = []
        self.negRule(rawpred, pred)
        dest = []
        qua = pred[0]
        if len(qua) == 1:
            val = 'x0'
            rep = 'A'
            if qua[0] == ('every', 'x0'):
                rep = 'a'
            self.recurTo(pred[-1], dest, val, rep)
        desttwo = []
        self.deleteSpareBracket(dest, desttwo)
        if pred[1] == 'not':
            desttwo = [pred[1], desttwo]
        val = self.arrowToOr(desttwo[-1])
        if val is not None:
            desttwo[-1] = val
        destthree = []
        self.deleteMiddleNeg(desttwo, destthree)
        destthree = destthree if len(destthree) > 0 else desttwo
        destthree = self.deleteArrow(destthree)
        destfour = []
        if type(destthree) == tuple:
            destfour = destthree
        else:
            self.adjustInfo(destthree, destfour)
        # print(destfour)
        return destfour

    def PredLog(self, sentence):
        pred = m.abstSent(sentence)
        res = self.predToStatement(pred)
        print(res)
        return res

predLogCtr = PredLogCtr()

class LogMgr(object):
    def __init__(self):
        self.ques = []
        self.res = []
        self.notUp = ['xor', 'not', 'and', 'or', 'arrow']

    def toUp(self, source):
        for i in range(len(source)):
            t = type(source[i])
            if t == list:
                self.toUp(source[i])
            elif t == tuple:
                source[i] = tuple([v.upper() if v not in self.notUp else v for v in source[i]])
            else:
                source[i] = source[i].upper() if source[i] not in self.notUp else source[i]
    
    def getRes(self, sentence):
        info = predLogCtr.PredLog(sentence)
        self.res.append(info)

    def getQues(self, sentence):
        info = predLogCtr.PredLog(sentence)
        self.ques.append(info)

    def reset(self):
        self.ques = []
        self.res = []

    def abstQues(self):
        info = self.ques[0]
        if len(info) == 3 and info[1] == 'and':
            return [info[0], info[2]]
        return info

    def abstRes(self):
        info = []
        res = []
        for a in self.res:
            if len(a) == 3 and a[1] == 'and':
                info += [a[0], a[2]]
            elif len(a) == 1:
                info += [a]
        for a in self.res:
            if len(a) == 3 and a[1] == 'xor':
                re = None
                for c in info:
                    print(c)
                    if c == a[0]:
                        re = a[0]
                    elif c == a[2]:
                        re = a[2]
                    elif len(a[0]) == 2 and c[0] == a[0][1]:
                        re = a[2]
                    elif len(a[2]) == 2 and c[0] == a[2][1]:
                        re = a[0]
                    elif len(c) == 2 and c[1] == a[0][0]:
                        re = a[2]
                    elif len(c) == 2 and c[1] == a[2][0]:
                        re = a[0]
                info.append(re)
        return info

    def analyze(self):
        self.toUp(self.res)
        self.toUp(self.ques)
        que = self.abstQues()
        info = self.abstRes()
        count = 0
        for a in info:
            if a in que:
                count += 1
        res = True if count == len(que) else False
        print(res)

    def debug(self):
        print(self.res)
        print(self.ques)

logMgr = LogMgr()

# m.abstConjs('他整天不是吃饭就是睡觉,活得真像一头猪。')
# m.abstConjs('我们不要美元，而要人名币。')
# m.abstConjs('我们不要空话，而要行动。')
# m.abstConjs('学术委员会的每个成员都是博士并且是教授。')

# m.abstComplex('他整天不是吃饭就是睡觉,活得真像一头猪。')
# m.abstComplex('我们不要美元，而要人名币。')
# m.abstComplex('我们不要空话，而要行动。')
# m.abstComplex('学术委员会的每个成员都是博士并且是教授。')

m.abstSent('任意的整数和任意的浮点数的乘积是浮点数。')
# m.abstSent('学术委员会的每个成员都是博士并且是教授。')
# m.abstSent('他整天不是吃饭就是睡觉,活得真像一头猪。')
# m.abstSent('我们不要美元，而要人名币。')
# m.abstSent('所有自然数是整数')
# m.abstSent('任何整数不是奇数就是偶数')
# m.abstSent('并非每个自然数是偶数。')
# m.abstSent('某些自然数是奇数。')

# predLogCtr.predToStatement([[('every', 'x0')], [('自然数', 'x0'), 'arrow', ('x0是整数',)]])

# predLogCtr.PredLog('任何整数不是奇数就是偶数')
# predLogCtr.PredLog('并非每个自然数是偶数。')
# predLogCtr.PredLog('所有自然数是整数')
# predLogCtr.PredLog('某些自然数是奇数。')

# logMgr.getRes('任何整数不是奇数就是偶数')
# logMgr.getRes('并非每个自然数是偶数')
# logMgr.getRes('所有自然数是整数')
# logMgr.getQues('某些自然数是奇数')
# logMgr.debug()
# logMgr.analyze()

# predLogCtr.PredLog('3的数量等于2的数量')
# predLogCtr.PredLog('如果里面有左小括号或右小括号，也必须构成小括号')
# predLogCtr.PredLog('不是水，就是火焰。')
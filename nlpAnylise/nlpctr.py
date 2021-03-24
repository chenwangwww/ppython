from ltp import LTP
ltp = LTP()

class NlpCtr(object):
    def __init__(self):
        pass

    def sdp_trans_res(self, strArr, sdpArr, posArr):
        tempstrArr = strArr[0]
        tempstrArr.insert(0, 'ROOT')
        tempposArr = posArr[0]
        tempposArr.insert(0, 'ROOT')
        tempsdpArr = sdpArr[0]

        tempArr = []
        for item in tempsdpArr:
            dic = {
                'dep': tempstrArr[item[0]],
                'gov': tempstrArr[item[1]],
                'type': item[2],
                'pos': tempposArr[item[0]]
            }
            tempArr.append(dic)
        return tempArr

    def trans_result(self, strArr, depArr, posArr):
        tempstrArr = strArr[0]
        tempstrArr.insert(0, 'ROOT')
        tempposArr = posArr[0]
        tempposArr.insert(0, 'ROOT')
        tempdepArr = depArr[0]

        tempArr = []
        for item in tempdepArr:
            dic = {
                'dep': tempstrArr[item[0]],
                'gov': tempstrArr[item[1]],
                'type': item[2],
                'pos': tempposArr[item[0]]
            }
            tempArr.append(dic)
        return tempArr

    def getHED(self, words):
        root = None
        for word in words:
            if word['gov'] == 'ROOT' and word['type'] == 'HED':
                root = word['dep']
        return root

    def getROOT(self, words):
        root = None
        for word in words:
            if word['gov'] == 'ROOT' and word['type'] == 'Root':
                root = word['dep']
        return root

    def getWord(self, words, GOV, wType):
        sbv = None
        for word in words:
            if word['type'] == wType and word['gov'] == GOV:
                sbv = word['dep']
        return sbv

    def getWordList(self, words, GOV, wType):
        slist = []
        for word in words:
            if word['type'] == wType and word['gov'] == GOV:
                slist.append(word['dep'])
        res = slist if len(slist) > 0 else None
        return res

    def getsdpList(self, words, wType, GOV = None):
        slist = []
        for word in words:
            if word['type'] == wType:
                if GOV is None:
                    slist.append(word)
                elif GOV == word['gov']:
                    slist.append(word['dep'])
        res = slist if len(slist) > 0 else None
        return res

    def get_att_pob(self, words, att_sbv):
        resl = []
        if att_sbv is not None:
            for a in att_sbv:
                word1 = self.getWord(words, a, 'ADV')
                word2 = self.getWord(words, word1, 'POB')
                res = word1 + word2 + a if word1 is not None and word2 is not None else None
                if res:
                    resl.append(res)
        return None if len(resl) == 0 else resl
    
    def abstractSentence(self, sentence):
        dic = None

        seg, hidden = ltp.seg([sentence])
        dep = ltp.dep(hidden)
        pos = ltp.pos(hidden)        

        words = self.trans_result(seg, dep, pos)
        if len(words) > 0:
            hed = self.getHED(words)
            if hed is not None:
                sbv = self.getWord(words, hed, 'SBV')
                vob = self.getWord(words, hed, 'VOB')
                fob = self.getWord(words, hed, 'FOB')
                adv = self.getWordList(words, hed, 'ADV')
                if adv is not None:
                    for a in adv:
                        pob = self.getWord(words, a, 'POB')
                        if a == '被' and sbv is None:
                            sbv = pob
                att_sbv = self.getWordList(words, sbv, 'ATT')
                attSS = self.get_att_pob(words, att_sbv)
                att_vob = self.getWordList(words, vob, 'ATT')  
                obj = list(filter(lambda x: x is not None, [vob, fob]))             
                dic = {
                    'subject': sbv,
                    'pred': hed,
                    'object': obj[0] if len(obj) > 0 else None,
                    'attS': att_sbv,
                    'attSS': attSS,
                    'attO': att_vob,
                    'adv': adv,
                }
        return dic

    def get_not_none(self, li):
        for i in li:
            if i is not None:
                return i
        return None

    def abstractSentence2(self, sentence):
        dic = None
        seg, hidden = ltp.seg([sentence])
        dep = ltp.dep(hidden)
        pos = ltp.pos(hidden)
        words = self.trans_result(seg, dep, pos)
        if len(words) > 0:
            hed = self.getHED(words)
            if hed is not None:
                coo_list = self.getWordList(words, hed, 'COO')
                sbv = self.getWord(words, hed, 'SBV')
                vob = self.getWord(words, hed, 'VOB')
                fob = self.getWord(words, hed, 'FOB')
                adv_list = self.getWordList(words, hed, 'ADV')
                pob = None
                if adv_list is not None:
                    for a in adv_list:
                        if a == '被':
                            pob = self.getWord(words, a, 'POB')
                att_sbv = self.getWordList(words, sbv, 'ATT')
                attSS = self.get_att_pob(words, att_sbv)
                att_vob = self.getWordList(words, vob, 'ATT')
                subject = self.get_not_none([sbv, pob])
                object = self.get_not_none([vob, fob])
                subject_coo_list = self.getWordList(words, subject, 'COO') if subject is not None else None
                object_coo_list = self.getWordList(words, object, 'COO') if object is not None else None
                dic = {
                    'subject': subject,
                    'pred': hed,
                    'object': object,
                    'attS': att_sbv,
                    'attSS': attSS,
                    'attO': att_vob,
                    'adv': adv_list,
                    'coo_list': coo_list,
                    'subject_coo_list': subject_coo_list,
                    'object_coo_list': object_coo_list,
                }
        return dic
                

    def abst_sent_sdp(self, sentence, abstDic):
        dic = None
        seg, hidden = ltp.seg([sentence])
        sdp = ltp.sdp(hidden)
        pos = ltp.pos(hidden)
        words_sdp = self.sdp_trans_res(seg, sdp, pos)
        if len(words_sdp) > 0:
            root = self.getROOT(words_sdp)
            if root is not None:
                agt = self.getsdpList(words_sdp, 'AGT', root)
                pat = self.getsdpList(words_sdp, 'PAT', root)
                tool = self.getsdpList(words_sdp, 'TOOL', root)
                loc = self.getsdpList(words_sdp, 'LOC')
                time = self.getsdpList(words_sdp, 'TIME', root)
                matl = self.getsdpList(words_sdp, 'MATL', root)
                mann = self.getsdpList(words_sdp, 'MANN', root)
                sco = self.getsdpList(words_sdp, 'SCO', root)
                reas = self.getsdpList(words_sdp, 'REAS', root)
                meas = self.getsdpList(words_sdp, 'MEAS')
                dic = {
                    'agt': agt,
                    'pat': pat,
                    'root': root,
                    'tool': tool,
                    'loc': loc,
                    'time': time,
                    'matl': matl,
                    'mann': mann,
                    'sco': sco,
                    'reas': reas,
                    'meas': meas,
                }
        return dic

    def abst_sent(self, sentence):
        res1 = self.abstractSentence2(sentence)
        res2 = self.abst_sent_sdp(sentence, res1)
        res3 = self.nlp_to_predlogistics(res1)
        print(res1)
        print(res2)
        print(res3)

    def nlp_to_predlogistics(self, dic):
        res = []
        actions = []
        quantifier = ('some', 'x') if dic['subject'] == '部分' else None
        if dic['attSS'] is not None:
            for i in dic['attSS']:
                actions.append((i, 'x'))
                actions.append('and')
        if dic['pred'] is not None and dic['object'] is not None:
            actions.append((dic['pred'] + dic['object'], 'x'))
        res.append([quantifier, tuple(actions)])
        return res

    def abstractComplex(self, sentence):
        dic_arr = []
        sents = sentence.split('，')
        sent_first = sents[0]
        dic = self.abstractSentence(sent_first)
        dic_arr.append(dic)
        for i in range(len(sents)):
            if i != 0:
                sent = sents[i]
                dic_other = self.abstractSentence(sent)
                if dic_other['subject'] is None:
                    dic_other['subject'] = dic['subject']
                dic_arr.append(dic_other)
        print(dic_arr)

class ComplexSentenceMgr(object):
    def __init__(self):
        self._nlpCtr = NlpCtr()
        self.keywords = {
            'binglie': [('不要', '而要')]
        }

    def getKeywords(self, subsent, type, index):
        res = None
        for item in self.keywords[type]:
            inde = subsent.find(item[index])
            if inde > -1:
                res = subsent[0:inde] + subsent[inde + len(item[index]):]
        return res

    def abstractBingLie(self, sentence):
        arr = sentence.split('，')
        for i in range(len(arr)):
            item = arr[i]
            res = self.getKeywords(item, 'binglie', 0)
            if res is not None:
                arr[i] = res
            else:
                res = self.getKeywords(item, 'binglie', 1)
                if res is not None:
                    arr[i] = res
        return arr

    def abstractSentence(self, sentence):
        dic_arr = []
        sents = self.abstractBingLie(sentence)
        sent_first = sents[0]
        dic = self._nlpCtr.abstractSentence(sent_first)
        dic_arr.append(dic)
        for i in range(len(sents)):
            if i != 0:
                sent = sents[i]
                dic_other = self._nlpCtr.abstractSentence(sent)
                if dic_other['subject'] is None:
                    dic_other['subject'] = dic['subject']
                dic_arr.append(dic_other)
        print(dic_arr)
        

nlpCtr = NlpCtr()
# nlpCtr.abstractSentence('妈妈用电饭煲煲汤。')
# nlpCtr.abstractSentence('我明天去哈尔滨。')
# nlpCtr.abstractSentence('小明昨天在哈尔滨生下一个小男孩。')
# nlpCtr.abst_sent('小明昨天在哈尔滨生下一个小男孩。')
# nlpCtr.abst_sent('学生们用纸折飞机。')
# nlpCtr.abst_sent('学生们用铅笔写字。')
# nlpCtr.abst_sent('军士齐声高喊。')
# nlpCtr.abst_sent('数学方面他是专家。')
nlpCtr.abst_sent('他因为酒驾被交警拘留了。')
# nlpCtr.abst_sent('周一早上升旗。')
# nlpCtr.abst_sent('一年有365天。')
# nlpCtr.abst_sent('在北京打工的不全是外地人。')
# nlpCtr.abst_sent('在北京打工的部分是外地人')
# nlpCtr.abst_sent('学术委员会的每个成员都是博士并且是教授。')

# nlpCtr.abstractComplex('我们不要空话，而要行动。')

# mgr = ComplexSentenceMgr()
# mgr.abstractSentence('我们不要空话，而要行动。')
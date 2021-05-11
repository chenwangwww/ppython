import re
from ComFuncs import *

class QuesRecognizer:
    def __init__(self):
        self._regexMapper = [
            Mode(r'.*有.*那.*是.*', [Rel('有'), Rel('是', {'subject': '那'})], 'self', Target({'pred':'有', 'target':'object'}, {'pred':'是', 'target':'subject'})),
            Mode(r'.*什么.*', [Rel('有', {'object': '什么'})], 'content', Target({'pred':'有', 'target':'object'}, {'pred':'是', 'target':'subject'})), 
        ]

    def fitMode(self, sent, sentMgr):
        for mode in self._regexMapper:
            print(mode.getAnswer(sent, sentMgr))
                
                
class Target:
    def __init__(self, des, sour):
        self._des = des
        self._sour = sour

    @property
    def des(self):
        return self._des

    @property
    def sour(self):
        return self._sour

class Rel:
    def __init__(self, predicate, other = {}):
        self._predicate = predicate
        self._other = other

    @property
    def predicate(self):
        return self._predicate

    @property
    def other(self):
        return self._other

class Mode(object):
    def __init__(self, regex, rels, type, target):
        self._regex = regex
        self._rels = rels
        self._type = type
        self._target = target

    @property
    def regex(self):
        return self._regex
    
    def fitMode(self, sent, sentMgr, knowledge = None):
        resReg = re.search(self._regex, sent)
        resRel = sentMgr.fitRels(self._rels)
        if resReg and resRel:
            return True
        else:
            return False
           
    def getAnswer(self, sent, sentMgr, knowledge = None):
        res = None
        if self.fitMode(sent, sentMgr, knowledge):
            if self._type == 'self':
                r = sentMgr.getInfo(self._target.des['pred'])
                if r:
                    res = [(self._target.des['target'], r[1][self._target.des['target']])]
                    r2 = sentMgr.getInfo(self._target.sour['pred'])
                    if r2:
                        res += [(self._target.sour['target'], r2[1][self._target.sour['target']])]
                        res += [('predicate', r2[0])]
        return res

quesRgr = QuesRecognizer()

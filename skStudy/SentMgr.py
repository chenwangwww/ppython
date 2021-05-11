from ComFuncs import *
class SentMgr(object):
    def __init__(self, info):
        self._info = {}
        for item in info:
            self._info[item[1]] = {}
            self._info[item[1]]['subject'] = item[0]
            self._info[item[1]]['object'] = item[2]

    @property
    def info(self):
        return self._info

    def getInfo(self, pred):
        keys = self._info.keys()
        r = findCW(pred, keys)
        if r:
            return [r, self._info[r]]
        else:
            return None
    
    def fitRels(self, rels):
        count = 0
        for rel in rels:
            keys = self._info.keys()
            r = findCW(rel.predicate, keys)
            if r:
                i = self._info[r]
                o = rel.other
                a, b = None, None
                if 'subject' in o:
                    a = i['subject'].find(o['subject']) > -1
                if 'object' in o:
                    b = i['object'].find(o['object']) > -1
                if a == False or b == False:
                    pass
                else:
                    count += 1
        if count == len(rels):
            return True
        else:
            return False
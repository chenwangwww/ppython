class PartCtr(object):
    def __init__(self) -> None:
        self._modes = [
            {'mode': ['n', 'nd', 'u', 'a', 'n'], 'res':[(0, 1, '有', 3, 4), (3, 4, '在', 0, 1)]},
            {'mode': ['n', 'nd', 'u', 'n'], 'res':[(0, 1, '有', 3), (3, '在', 0, 1)]},
            {'mode': ['a', 'n', 'k', 'p', 'n', 'nd'], 'res':[(4, 5, '有', 0, 1, 2)]},
        ]
        self._dataBase = []

    def segment(self, asub, alist, wordlist):
        asubStr = '&'.join(asub)
        alistStr = '&'.join(alist)
        count = alistStr.count(asubStr)
        indices = []
        res = []
        startIndex = 0
        for i in range(count):
            index = alistStr.find(asubStr, startIndex)
            listIndex = len(alistStr[:index].split('&')) - 1
            indices.append(listIndex)
            startIndex += len(asubStr)
        for ii in indices:
            res.append(wordlist[ii: ii + len(asub)])
        res = res if len(res) > 0 else None
        return res

    def useModeRes(self, modeRes, r):
        res = []
        for rr in r:
            for mm in modeRes:
                sub = ''
                for m in mm:
                    sub += rr[m] if type(m) == int else m
                res.append(sub)
        return res
    
    def validateMode(self, alist, wordlist):
        res = []
        for m in self._modes:
            mode = m['mode']
            r = self.segment(mode, alist, wordlist)
            if r:
                res += self.useModeRes(m['res'], r)
        return res

partCtr = PartCtr()
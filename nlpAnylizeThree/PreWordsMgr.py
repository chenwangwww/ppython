import re

class PreWordsMgr(object):
    def __init__(self):
        with open('user_dict.txt', 'r', encoding='utf-8') as f:
            self._lines = f.readlines()
            self._lines = [v.strip() for v in self._lines]
            self._lines.sort(key=lambda a: len(a))
            self._lines.reverse()
            self.reps = []
            self.ordN = 64

    def bInReps(self, original):
        res = list(filter(lambda a: a[0] == original, self.reps))
        return len(res) > 0

    def getOriginal(self, rep):
        res = list(filter(lambda a: a[1] == rep, self.reps))
        res = res[0][0] if len(res) > 0 else None
        return res

    def getRealName(self, rep):
        name = self.getOriginal(rep)
        if name is None:
            name = rep
        return name

    def getRep(self, original):
        res = list(filter(lambda a: a[0] == original, self.reps))
        if len(res) == 0:
            self.ordN += 1
            res = [chr(self.ordN), True]
        else:
            res = [res[0][1], False]
        return res
    
    def doSpecialWords(self, sent):
        pattern = re.compile(r'".*?"')
        m = pattern.search(sent)
        if m is not None:
            span = m.span()            
            ori = sent[span[0]+1:span[1]-1]
            chrS, r = self.getRep(ori)
            if r:
                self.reps.append((ori, chrS))
            sent = sent[:span[0]] + chrS + sent[span[1]:]
            self.doSpecialWords(sent)
        # print(sent)
        return sent
    
    def doWords(self, sent):
        sent = self.doSpecialWords(sent)
        for word in self._lines:
            count = sent.count(word)
            if count > 0:
                chrS, r = self.getRep(word)
                sent = sent.replace(word, chrS)
                if r:
                    self.reps.append((word, chrS))
        # print(sent)
        return sent


mgr = PreWordsMgr()
# mgr.doWords('每一位是整数')
# mgr.doSpecialWords('"（"是左小括号"（"')

# match = re.sub(r'(".*?")', 'A', '"（"是左小括号"（"')
# print(match)
# obj = re.search(r'".*?"', '"（"是左小括号"（"')
# print(obj.span())

# sent = '"（"是左小括号"（"'
# pattern = re.compile(r'".*?"')
# m = pattern.search(sent)
# print(m.span())
# sent = sent[:m.span()[0]] + 'A' + sent[m.span()[1]:]
# print(sent)
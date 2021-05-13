import re
from ltp import LTP
ltp = LTP()

class Master():
    def __init__(self) -> None:
        self._name = ''
        self._atts = []
        self._feel = {}

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def atts(self):
        return self._atts
    @atts.setter
    def atts(self, value):
        self._atts = value
    
    @property
    def feel(self):
        return self._feel
    @feel.setter
    def feel(self, value):
        if value not in self._feel:
            item = {value:{}}
            self._feel.update(item)

    def setOneFeel(self, feel, object, value):
        if feel not in self._feel:
            print('该主体没有这种情感！')
            return
        self._feel[feel].update({object: value})

def func1(groups):
    print('这是问句。')

def func2(groups):
    master_name = groups[0]
    feel1, feel2 = groups[1], groups[3]
    object1, object2 = groups[2], groups[4]
    master = Master()
    master.name = master_name
    master.feel = feel1
    if feel2[0] == '更':
        master.setOneFeel(feel1, object1, 1)
        master.setOneFeel(feel1, object2, 2)
        print(master.feel)


class PatternMgr():
    def __init__(self) -> None:
        self._patterns = [
            r'.+\？$',
            r'(.+?)&(爱)&(.+?)，(&更&爱&)(.+?)[，。].*'
        ]
        self._reacts = [
            func1,
            func2
        ]

    def checkPattern(self, sent):
        seg, hidden = ltp.seg([sent])
        sent = '&'.join(seg[0])
        length = len(self._patterns)
        for i in range(length):
            p = self._patterns[i]
            ret = re.match(p, sent)
            if ret:
                func = self._reacts[i]
                groups = ret.groups()
                groups = [val.replace('&', '') for val in groups]
                func(groups)

sent = '你好吗？'
sent = '我爱学校，更爱学校的四季。'
patternMgr = PatternMgr()
patternMgr.checkPattern(sent)
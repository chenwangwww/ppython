class Mapper(object):
    def __init__(self):
        self._teachMap = [
            ('是', 'obj.pushMember(subj.name)'),
        ]
        self._teachModeMap = [
            '每一位',
            '是',
            '首位',
            '末位',
        ]

    def getMap(self, word):
        res = list(filter(lambda a: a[0] == word, self._teachMap))
        res = res[0][1] if len(res) > 0 else None
        return res

    def getModeMap(self, word):
        res = word if word in self._teachModeMap else None
        return res

mapper = Mapper()
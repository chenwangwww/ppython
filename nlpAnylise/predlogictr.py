from nlpctrFour import NlpCtr

nlpCtr = NlpCtr()

class Mapper(object):
    def __init__(self):
        self.map = {
            'Quantifiers': [
                ['所有', [('ATT', 'subject'), ('ATT', 'object')], 'every'],
                ['都', [('ADV', 'pred')], 'every'],
                ['每个', [('ATT', 'subject'), ('ATT', 'object')], 'every']
            ],
            'Negatives': [
                ['并非', [('ADV', 'pred')], 'not'],
                ['不', [('ADV', 'pred')], 'not']
            ],
            'Conjunctions': [
                ['并且', [('ADV', 'pred')], 'and'],
                ['而', [('ADV', 'pred')], 'and']
            ],
        }

    def getMaps(self, words, SEG, wType):
        res = []
        for word in words:
            a = self.getMap(word, SEG, wType)
            if a is not None:
                res.append(a)
        res = res if len(res) > 0 else None
        return res

    def getMap(self, word, SEG, wType):
        maps = self.map.items()
        for map in maps:
            mapValues = map[1]
            for mapValue in mapValues:
                w = nlpCtr.indexToWord(word['dep'], SEG)
                if w == mapValue[0] and (word['type'], wType) in mapValue[1]:
                    return [map[0], mapValue[2], word]
        return None

mapper = Mapper()
# [('some', 'x'), ('A', 'x'), 'not']  'and'
class PredLogCtr(object):
    def __init__(self):
        pass

    def nlpToPredLog(self, sentence):
        resNlp = nlpCtr.abstractSentence(sentence)
        if resNlp is not None:
            for item in resNlp:
                res = {
                    'quantifier': None,
                    'function': None,
                    'negative': None
                }
                conjunction = None
                wordIndices = [item['pred']]
                related = item['related']
                if related is not None:
                    for r in related:




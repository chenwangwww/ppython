from ltp import LTP
ltp = LTP()
from NlpCtr import nlpCtr
import re

paragraph = """
在美丽的旌湖旁，坐落着德阳市实验小学校。

一进校门，看到四周有几座高大的教学楼，分别是真全楼、真玉楼、真思楼、真问楼、真学楼。穿过真玉楼来到了我们篮球场和乒乓球场，又穿过乒乓球场就来到了红红的跑道上。跑道像一大片红领巾似的，向前走来到了升旗台。每到星期一的时候，全校同学在升旗台下一起唱国歌。这是一所非常美丽的学校！

春天，学校的树木和小草开始发芽了，到处鸟语花香，生机勃勃。漂亮的李花开了，白白的，像花仙子正在翩翩起舞似的。

夏天，学校树木的叶子长得又多又密，像撑开的大伞，给我们遮阳避暑。小草也长得多绿多茂密啊！真像一块绿油油的地毯。

秋天，花草凋落，秋姑娘把树上的叶子涂成了黄色。同学们都喜欢把捡来的银杏叶做成书签。枫叶也渐渐地变成红色，枫叶像手掌一样，真美丽啊！

冬天，天气越来越冷了，我们穿的可厚了。树上的叶子打了一层厚厚的霜。霜是白色的，摸一下就会掉。霜真的好神奇啊！

我爱学校，更爱学校的四季，学校的四季就像画家笔下的四季图一样，美丽而迷人。
"""
# paragraph = '学校和学校的四季，你比较喜欢哪个？'
paragraph = '我爱学校，更爱学校的四季。'
# paragraph = '冰箱里的饮料是奶茶，还是柳橙汁？'
# paragraph = '今天的晚餐是要吃面，还是要吃汉堡？'
# sents = ltp.sent_split([paragraph])
# for sent in sents:
#     print(sent)


seg, hidden = ltp.seg([paragraph])
paragraph = '&'.join(seg[0])
print(paragraph)
# pattern = r'(.+)是(.+)，还是(.+?)[？。]{0,}$'       #今天的晚餐是要吃面，还是要吃汉堡？
# pattern = r'(.+)&和&(.+)，(.+比较.+)[？。]{0,}$'       #学校和学校的四季，你比较喜欢哪个？
pattern = r'(.+?)&(爱)&(.+?)，(&更&爱&)(.+?)[，。].*'       #我爱学校，更爱学校的四季，学校的四季就像画家笔下的四季图一样，美丽而迷人。
ret = re.match(pattern, paragraph)
if ret:
    print(ret.groups())
    groups = ret.groups()
    for g in groups:
        info = nlpCtr.abstractSentence(g.replace('&', ''))
        print('g:', info)

# sent = '我爱学校，更爱学校的四季。'
# seg, hidden = ltp.seg([sent])
# pos = ltp.pos(hidden)
# dep = ltp.dep(hidden)
# print(seg)
# print(pos)
# print(dep)
# print(nlpCtr.abstractSentence(sent))

class Master():
    def __init__(self) -> None:
        self._name = ''
        self._atts = []

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
    def 爱(self):
        return self._爱
    @爱.setter
    def 爱(self, value):
        self._爱 = value

class AttCrtr():
    def __init__(self) -> None:
        pass

    def getATTs(self, sent):
        res = []
        seg, hidden = ltp.seg([sent])
        dep = ltp.dep(hidden)
        pos = ltp.pos(hidden)
        words = nlpCtr.trans_result(dep, pos)
        hed = nlpCtr.getHED(words)
        attsHed = [hed]
        self.getWordAtts(hed, words, attsHed)
        if len(attsHed) > 1:
            res.append(attsHed)
        for word in words:
            if word['type'] == 'ATT' and word['gov'] != hed:
                atts = [word['gov']]
                self.getWordAtts(word['gov'], words, atts)
                if len(atts) > 1:
                    res.append(atts)
        for r in res:
            m = Master()
            m.name = seg[0][r[0]-1]
            m.atts = self.indicesToWords(r[1:], seg)
            print('m:', m.name, m.atts)


    def getWordAtts(self, GOV, words, res):  
        for word in words:
            if word['gov'] == GOV:
                if word['type'] == 'ATT':
                    att = word['dep']
                    res.append(att)
                    self.getWordAtts(att, words, res)

    def indicesToWords(self, indices, seg):
        indices.sort()
        res = []
        for index in indices:
            res.append(seg[0][index - 1])
        return res


# attCrtr = AttCrtr()
# attCrtr.getATTs('冰箱里的饮料')


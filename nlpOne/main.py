from NlpCtr import nlpCtr
from ModeCtr import modeCtr

paragraph = """
在我们的校园里有一处美丽的景色，那就是校园的鱼池。

走在池塘的小桥上，一股清风吹过，是那么舒服。鱼儿们在池塘里欢快地游泳，有的鱼儿在唱歌，有的鱼儿在做游戏。

当“喷泉”把水喷出来，小鱼急急忙忙“跑”过去，洗一个澡。小鱼洗完澡后总会找它最好的朋友来玩耍。鱼妈妈呢？鱼妈妈自由自由地游过来游过去，等着小鱼回家。

小鱼们在池塘里快乐、开心地玩耍着，池塘就是小鱼的家。每当我走过池塘上的小桥，都会不由自主地看着那些小鱼，它们玩得多么开心、多么快乐。

这是校园一处难以忘怀的景色。
"""

questions = [
    '在我们的校园里有鱼池吗？',
    '在我们的校园里有什么？',
    '鱼池美丽吗？',
    '池塘里没有小鱼吗？',
    '池塘上有小桥吗？',
    '小鱼们快乐吗？',
    '小鱼们不快乐吗？',
]

paraList = nlpCtr.paragraphToList(paragraph)
modeCtr.learn(paraList)
for q in questions:
    datas = nlpCtr.abstractSentence(q)
    modeCtr.question(datas)


# nlpCtr.abstractSentence('鱼儿们在池塘里欢快地游泳，有的鱼儿在唱歌，有的鱼儿在做游戏。')


# ('池塘就是小鱼的家', '小鱼的家在池塘')
# ('池塘上的小桥', '池塘上有小桥', '小桥在池塘上')
# ('壮丽的祖国大地')
# ('一把锋利的剑')
# ('池塘里有小鱼吗？')
# ('他们不是为了自我陶醉而工作')
# ('小鱼们在池塘里')
# ('房间里的床', '房间里有床', '床在房间里')

# sent = '他们不是为了自我陶醉而工作'
# from ltp import LTP
# ltp = LTP()
# seg, hidden = ltp.seg([sent])
# pos = ltp.pos(hidden)
# dep = ltp.dep(hidden)
# print(seg)
# print(pos)
# print(dep)
# print(nlpCtr.abstractSentence(sent))


# (['池塘', '上', '的', '小', '桥'], ['n', 'nd', 'u', 'a', 'n'], [(4, 5, 'ATT'), (5, 8, 'ATT'), (6, 5, 'RAD'), (7, 8, 'ATT')])
# (['一', '把', '锋利', '的', '剑'], ['m', 'q', 'a', 'u', 'n'], [(1, 2, 'ATT'), (2, 5, 'ATT'), (3, 5, 'ATT'), (4, 3, 'RAD')])
# (['壮丽', '的', '祖国', '大地'], ['a', 'u', 'n', 'n'], [(1, 4, 'ATT'), (2, 1, 'RAD'), (3, 4, 'ATT')])
# (['小', '鱼', '的', '家', '在', '池塘'], ['a', 'n', 'u', 'n', 'v', 'n'], [(1, 2, 'ATT'), (2, 4, 'ATT'), (3, 2, 'RAD'), (4, 5, 'SBV'), (5, 0, 'HED'), (6, 5, 'VOB')])
# (['房间', '里', '的', '床'], ['n', 'nd', 'u', 'n'], [(1, 2, 'ATT'), (2, 4, 'ATT'), (3, 2, 'RAD')])
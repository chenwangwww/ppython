content = """
在我们的校园里有一处美丽的景色，那就是校园的鱼池。

走在池塘的小桥上，一股清风吹过，是那么舒服。鱼儿们在池塘里欢快地游泳，有的鱼儿在唱歌，有的鱼儿在做游戏。

当“喷泉”把水喷出来，小鱼急急忙忙“跑”过去，洗一个澡。小鱼洗完澡后总会找它最好的朋友来玩耍。鱼妈妈呢？鱼妈妈自由自由地游过来游过去，等着小鱼回家。

小鱼们在池塘里快乐、开心地玩耍着，池塘就是小鱼的家。每当我走过池塘上的小桥，都会不由自主地看着那些小鱼，它们玩得多么开心、多么快乐。

这是校园一处难以忘怀的景色。
"""

questions = [
    '我们的校园有什么？',
    '我们的校园有鱼池吗？',
    '鱼池美丽吗？',
    '鱼池有小鱼吗？',
    '池塘上有小桥吗？',
    '池塘里有“喷泉”吗？',
    '池塘里的小鱼们快乐吗？',
]

# 在我们的校园里有一处美丽的景色，那就是校园的鱼池。-> 
# [在我们的校园里, 有 [一处美丽的景色， 是，校园的鱼池 ]]

# from ltp import LTP
# ltp = LTP()
# seg, hidden = ltp.seg(['在我们的校园里有一处美丽的景色，那就是校园的鱼池。'])
# pos = ltp.pos(hidden)
# dep = ltp.dep(hidden)
# print(seg)
# print(pos)
# print(dep)

from NlpCtr import nlpCtr
from SentMgr import SentMgr
from QuesRecognizer import quesRgr
from ComFuncs import *

# nlpCtr.abstractSentence('妈妈是一个可爱的人，她有一双灵巧的手。')

sentC = '在我们的校园里有一处美丽的景色，非常有人气，那就是校园的鱼池。'
# sentC = '我们的校园有什么？'
infosC = nlpCtr.abstractSentence(sentC)
sentMgr = SentMgr(infosC)
quesRgr.fitMode(sentC, sentMgr)

# resC = []
# sentC = '在我们的校园里有一处美丽的景色，那就是校园的鱼池。'
# infosC = nlpCtr.abstractSentence(sentC)
# for i in infosC:
#     resC.append(SentMgr(i))

# res = []
# sent = '我们的校园有鱼池吗？'
# infos = nlpCtr.abstractSentence(sent)
# for i in infos:
#     res.append(SentMgr(i))

# resRgr = None
# for sentMgr in res:
#     s = quesRgr._regexMapper[0].fitMode(sent, sentMgr)
#     if s:
#         resRgr = [s, sent, sentMgr]
#         break

# ress = None
# s = resRgr[0]
# for i in resC:
#     info = resRgr[2].info
#     infoi = i.info
#     if s == 'obj':
#         if infoi['subj'] != '' and info['subj'] in infoi['subj'] and \
#             info['pred'] in infoi['pred']:
#             ress = infoi['obj']
#         if infoi['subj'] == '' and info['subj'] in infoi['pred'] and \
#             info['pred'] in infoi['pred']:
#             ress = infoi['obj']
#     elif s == 'subj':
#         if infoi['subj'] != '' and info['obj'] in infoi['subj'] and \
#             info['pred'] in infoi['pred']:
#             ress = infoi['obj']
#         if infoi['subj'] == '' and info['obj'] in infoi['pred'] and \
#             info['pred'] in infoi['pred']:
#             ress = infoi['obj']

# print(ress)

# '在我们的校园里有一处美丽的景色，那就是校园的鱼池。'
# ['', '在我们的校园里有', '一处美丽的景色', '那', '就是', '校园的鱼池']
# r'.*有.*那.*是.*'
# [['有', 'pred'], ['那', 'subj', {'target': 'obj'}], ['是', 'pred']]
# =>
# ['那', '一处美丽的景色']
# 校园的鱼池 一处美丽的景色
# 在我们的校园里有 校园的鱼池
# [0,1,2,3,4,5]
# [3,2]
# [5,2]
# [1,5]

[['', '在我们的校园里有', '一处美丽的景色'], ['', '非常有', '人气'], ['那', '就是', '校园的鱼池']]
=》
core: ['', '在我们的校园里有', '一处美丽的景色']
rest: ['', '非常有', '人气'], ['那', '就是', '校园的鱼池']
map: {
    'condition': ('predicate': '.*有.*') in core
    'result': core['object'] is 'subject' of rest
}

[['我们的校园', '是', '一处美丽的景色'], ['', '非常有', '人气']]
=》
core: ['我们的校园', '是', '一处美丽的景色']
rest: ['', '非常有', '人气']
map: {
    'condition': ('predicate': '.*是.*') in core
    'result': core['subject'] is 'subject' of rest
}


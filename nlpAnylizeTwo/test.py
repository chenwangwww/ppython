import pickle
from ltp import LTP
ltp = LTP()
from PreWordsMgr import mgr
from NlpCtr import nlpCtr
from Mapper import mapper
from ClsCreater import ClsCreater
from DbCtr import ctr
from TeachModeMap import *

TBNAME = "chen_info"

def getItem(id):
    item = None
    query = ctr.queryData(TBNAME, id)
    if query:
        item = pickle.loads(query[1])
    else:
        item = ClsCreater(id)
    return item

def smartUpDb(item):
    query = ctr.queryData(TBNAME, item.name)
    if query:
        ctr.updateData(TBNAME, item.name, pickle.dumps(item))
    else:
        ctr.insertData(TBNAME, {'id':item.name, 'sequence':pickle.dumps(item)})

sentences = ['']*12
sentences[0] = '每一位是整数'
sentences[1] = '1是整数'
sentences[2] = '0是整数'
sentences[3] = '"("是左小括号'
sentences[4] = '")"是右小括号'
sentences[5] = '左小括号的数量等于右小括号的数量'
sentences[6] = '首位是左小括号'
sentences[7] = '末位是右小括号'
sentences[8] = '"+"是加号'
sentences[9] = '"-"是减号'
sentences[10] = '"*"是乘号'
sentences[11] = '"/"是除号'

for i in range(len(sentences)):
    sentences[i] = mgr.doWords(sentences[i])

# for s in sentences:
#     seg, hidden = ltp.seg([s])
#     pos = ltp.pos(hidden)
#     dep = ltp.dep(hidden)
#     print(seg)
#     print(pos)
#     print(dep)
# print(mgr.reps)

def teach(sent):
    sent = mgr.doWords(sent)
    info = nlpCtr.abstractSentence(sent)
    subj = getItem(mgr.getRealName(info['subject']))
    obj = getItem(mgr.getRealName(info['object']))
    hedFunc = mapper.getMap(info['pred'])
    exec(hedFunc, {'subj':subj, 'obj':obj})
    smartUpDb(subj)
    smartUpDb(obj)
    # print(obj.members)
    return subj, obj

# teach('"+"是加号')
# teach('"-"是减号')
# teach('"*"是乘号')
# teach('"/"是除号')
# teach('"("是左小括号')
# teach('")"是右小括号')

def teachMode(sent, target = None):
    sent = mgr.doWords(sent)
    info = nlpCtr.abstractSentence(sent)
    obj = getItem(mgr.getRealName(info['object']))
    subjFunc = mapper.getModeMap(mgr.getRealName(info['subject']))
    hedFunc = mapper.getModeMap(info['pred'])
    if subjFunc and hedFunc:
        tar = obj if target is None else getItem(target)
        mode = tar.mode
        mode += [(subjFunc + hedFunc, obj.name)]
        tar.setMode(mode)
    smartUpDb(tar)

def teachMode2(sent, target):
    sent = mgr.doWords(sent)
    info = nlpCtr.abstractSentence(sent)
    hedFunc = mapper.getModeMap(info['pred'])

def modeAction(mode):
    m = eval(mode)
    return m

# teachMode('每一位是整数')
# print(getItem('整数').mode)
# getItem('整数').bCls('12345#@4', 0, modeAction, getItem)

# cls = ClsCreater('小括号')
# smartUpDb(cls)

# teachMode('首位是左小括号', '小括号')
# teachMode('末位是右小括号', '小括号')
# print(getItem('小括号').mode)

resInfo = []
lens = 0
def abstSent(sent):
    global lens
    # count = getItem('整数').bCls(sent, 0, modeAction, getItem)
    count = getItem('小括号').bCls(sent, 0, modeAction, getItem)
    resInfo.append(sent[lens:lens+count])
    lens += count
# abstSent('12+(5-4)*(5+4)')
# print(resInfo)

# abstSent('(5-4)*(5+4)')
# print(resInfo)

# print(getItem('左小括号').members), print(getItem('右小括号').members)

# from TeachModeMap import 是
# print(是('chenw'))


# mode = ['是']
# for f in mode:
#     eval(f)()
# --------------------------------------------

# from nlpctrFour import NlpCtr

# nlpCtr = NlpCtr()

# res = nlpCtr.abstractSentence('1和2.0是数字')
# print(res)

# --------------------------------------------

# from nlpctrFive import m

# print(m.abstSent('1和2是数字'))

# --------------------------------------------
# from ClsCreater import ClsCreater

# intCls = ClsCreater()
# intCls.pushMember(0)
# intCls.pushMember(1)
# intCls.pushMember(2)
# intCls.pushMember(3)
# intCls.pushMember(4)
# intCls.pushMember(5)
# intCls.pushMember(6)
# intCls.pushMember(7)
# intCls.pushMember(8)
# intCls.pushMember(9)

# res = intCls.bMember(2)
# print(res)

# print('123'[2:3])

# for i in range(10):
#     if i == 5:
#         continue
#     print(i)

# --------------------------------------------

from inspect import signature

def 每一位(content, obj, func):
    length = len(content)
    count = 0
    for i in list(content):
        if func(i, obj):
            count += 1
    return length == count

def 首位(content, obj, func):
    length = 1
    count = 0
    if func(content[0], obj):
        count += 1
    return length == count

def 末位(content, obj, func):
    length = 1
    count = 0
    if func(content[-1], obj):
        count += 1
    return length == count

def 数量(content, att):
    return content.count(att.members[0])

def 等于(subj, obj):
    return subj == obj

def 是(arg1, arg2):
    return arg2.bMember(arg1)

def teachMode3(sent, target = None):
    sent = mgr.doWords(sent)
    info = nlpCtr.abstractSentence(sent)
    # obj = getItem(mgr.getRealName(info['object']))
    subjFunc = mapper.getModeMap(mgr.getRealName(info['subject']))
    objFunc = mapper.getModeMap(mgr.getRealName(info['object']))
    hedFunc = mapper.getModeMap(info['pred'])
    
    



    # hedFunc = mapper.getModeMap(info['pred'])
    # if subjFunc and hedFunc:
    #     tar = obj if target is None else getItem(target)
    #     mode = tar.mode
    #     mode += [(subjFunc + hedFunc, obj.name)]
    #     tar.setMode(mode)
    # smartUpDb(tar)

def mapToFunc(subjFunc, objFunc, hedFunc, info, content):
    if subjFunc:
        sig = signature(subjFunc)
        arr = list(dict(sig.parameters).keys())
        print(arr)
        if 'att' in arr and 'func' not in arr:
            subj = subjFunc(content, getItem(info['attSubj']))
            obj = objFunc(content, getItem(info['attObj']))
        elif 'obj' in arr and 'func' in arr:
            print(subjFunc(content, getItem(info['object']), hedFunc))

mapToFunc(每一位, None, 是, {'object':'整数'}, '$123%')
mapToFunc(首位, None, 是, {'object':'左小括号'}, '($123%')
mapToFunc(末位, None, 是, {'object':'右小括号'}, '($123%)')
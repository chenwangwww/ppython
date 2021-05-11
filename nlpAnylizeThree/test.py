from ActionMap import *
from ModeMap import *
from TeachMap import *
from PreWordsMgr import mgr
from inspect import signature
from DbCtr import ctr
from ClsCreater import ClsCreater
from NlpCtr import nlpCtr
import pickle
from ltp import LTP
ltp = LTP()

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
        ctr.insertData(
            TBNAME, {'id': item.name, 'sequence': pickle.dumps(item)})


def getArgs(mode):
    m = eval(mode)
    sig = signature(m)
    arr = list(dict(sig.parameters).keys())
    return arr

# ('ModeMap', '是')
def bCls(content, mode):
    m = eval(mode)
    arr = getArgs(mode)
    dic = {}
    for i in arr:
        dic[i] = eval(i) 
    print(m(**dic))

# ('ActionMap', '左边、右边')
def getRes(content, action, symbolIndex):
    m = eval(action)
    arr = getArgs(action)
    dic = {}
    for i in arr:
        dic[i] = eval(i)
    print(m(**dic))

# ('TeachMap', '是')
def teach(pred, subj, obj):
    m = eval(pred)
    arr = getArgs(pred)
    dic = {}
    for i in arr:
        dic[i] = eval(i)
    subjIns, objIns = m(**dic)
    smartUpDb(subjIns)
    smartUpDb(objIns)

# ('ActionMap', '数量')
def actionAtt(core, ATT, content):
    m = eval(core)
    arr = getArgs(core)
    dic = {}
    for i in arr:
        dic[i] = eval(i)
    res = m(**dic)
    print(res)
    return res

def anylize(sent):
    # sent = mgr.doWords(sent)
    info = nlpCtr.abstractSentence(sent)
    subj = info['subject']
    obj = info['object']
    hed = info['pred']
    attSubj = info['attSubj']
    attObj = info['attObj']
    if hed and subj and obj:    
        hed = 'teach_' + info['pred']   
        teach(hed, subj, obj)

def anylize2(sent, content):
    info = nlpCtr.abstractSentence(sent)
    subj = info['subject']
    obj = info['object']
    hed = info['pred']
    attSubj = info['attSubj']
    attObj = info['attObj']
    subjRes = None
    objRes = None
    if subj and attSubj and content:
        subjRes = actionAtt('action_' + subj, attSubj, content)
    if obj and attObj and content:
        objRes = actionAtt('action_' + obj, attObj, content)
    if hed and subjRes and objRes:
        m = eval(hed)
        arr = getArgs(hed)
        dic = {}
        for i in arr:
            dic[i] = eval(i)
        res = m(**dic)
        print(res)


# bCls('14568', '整数')
# getRes('12+3', 'action_左边', 2)
# getRes('12+3', 'action_右边', 2)
# teach('teach_是', 1, '整数')

# anylize('0是整数')
# anylize('1是整数')
# anylize('2是整数')
# anylize('3是整数')
# anylize('4是整数')
# anylize('5是整数')
# anylize('6是整数')
# anylize('7是整数')
# anylize('8是整数')
# anylize('9是整数')

# bCls('145%68', '整数')
# actionAtt('action_数量', '1', '1129939')

# ('首位是左小括号', '小括号')
# ('末位是右小括号', '小括号')
# ('左小括号的数量等于右小括号的数量', '小括号')
# ('如果里面有左小括号或右小括号，也必须构成小括号', '小括号')

anylize2('3的数量等于2的数量', '23355')
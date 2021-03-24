from NeureCtr import NeureCtr
from Geo import CoorSystem, np
geo = CoorSystem()
# from ltp import LTP
# ltp=LTP()

# sentence = '小明在楼上'
# seg,hidden = ltp.seg([sentence])
# sdp = ltp.sdp(hidden)
# dir_txt = ''
# for item in sdp[0]:
#     if item[2] == 'LOC':
#         txt = seg[0][item[0]-1]
#         dir_txt = geo.judge_dir_by_txt(txt)
# text = geo.action_by_txt(dir_txt, '接近')
# print(text)

#小明在楼上

#小明在隔壁

#小明在二楼，我在一楼 =》 二楼 一楼 
#楼层数字越大，越高，二大于一，所以小明在楼上
# （小明，二楼）（我，一楼）
# 楼{

# }
#数字大的楼层在数字小的楼层的上面

#小明在小红的前面，小红在小兰的前面 =>小明在小兰的前面
#a = 在前面（小明，小红）  b = 在前面（小红，小兰） and a[1]=b[0]  =》 在前面（小明，小兰）
# sentence1 = '小明在小红的前面'
# sentence2 = '小红在小兰的前面'
# sentence3 = '小明在小兰的前面'

# def func(sentence):
#     seg,hidden = ltp.seg([sentence])
#     dep = ltp.dep(hidden)
#     pred = None
#     subject = None
#     object = None
#     att = None
#     for item in dep[0]:
#         if item[2] == 'HED':
#             pred = item[0]
#     for item in dep[0]:
#         if item[2] == 'SBV' and item[1] == pred:
#             subject = item[0]
#         elif item[2] == 'VOB' and item[1] == pred:
#             object = item[0]
#     for item in dep[0]:
#         if item[2] == 'ATT' and item[1] == object:
#             att = item[0]
#     return (seg[0][subject-1], seg[0][att-1], seg[0][pred-1] + seg[0][object-1])
# print(func(sentence1))
# print(func(sentence2))
# print(func(sentence3))

# sentences = """
# a,b
# def s():
#     if a[1] == b[0]:
#         print (a[0], b[1], b[2])
# s()
# """
# exec(sentences, {'a': func(sentence1), 'b': func(sentence2)})
# sentence = '在北京打工的不全是外地人'
# seg,hidden = ltp.seg([sentence])
# pos = ltp.pos(hidden)
# sdp = ltp.sdp(hidden)
# srl = ltp.srl(hidden, keep_empty=False)
# dep = ltp.dep(hidden)
# print(seg)
# print(pos)
# print(sdp)
# print(srl)
# print(dep)

# class person(object):
#     def __init__(self, name, bmember, bdoctor, byong):
#         self._bm = bmember
#         self._bd = bdoctor
#         self._by = byong   
#         self._name = name   

# list1 = [
#     person('chen', True, True, True),
#     person('lisa', True, False, True),
#     person('xiaoming', True, True, True),
# ]
# def A(x):
#     return x._bm
# def B(x):
#     return x._bd
# def C(x):
#     return x._by

# def exist(vals, func1, func2, func3):
#     res = False
#     for val in vals:
#         if func1(val) and func2(val) and func3(val):
#             res = True
#     return res

# res = exist(list1, A,B,C)
# print(res)

# 学术委员会的每个成员都是博士并且是教授。
# 成员{
#     ‘是’：[（‘’，[‘学术委员会’, ‘每个’]，‘博士’）， （‘’，[‘学术委员会’， ‘每个’]，‘教授’）]
# }
# 小明是学术委员会的成员
# 小明{
#     ‘是’：[(‘’， ‘’， （‘学术委员会’， ‘成员’ ， ‘ATT’）),
#             (‘’，‘’，‘博士’)，
#             (‘’，‘’，‘教授’)]
# }

# (∀x)(F(x)→G(x)
# (ヨx)(F(x)∧G(x))
# ┓、∧、∨、→和↔
#-------------------------#既是博士，又是教授---------------------------
# (∀x)(F(x)∧G(x)
# neureCtr1 = NeureCtr('小明')
# neureCtr1.relevants = ['是', ('', '', '博士')]
# neureCtr1.relevants = ['是', ('', '', '教授')]

# neureCtr2 = NeureCtr('陈霞')
# neureCtr2.relevants = ['是', ('', '', '博士')]
# neureCtr2.relevants = ['是', ('', '', '教授')]

# neureCtr3 = NeureCtr('丽莎')
# neureCtr3.relevants = ['是', ('', '', '博士')]
# neureCtr3.relevants = ['是', ('', '', '教授')]

# def every(vals, pred, item1, item2):
#     for val in vals:
#         res1 = val.relevants[pred].count(item1) > 0
#         res2 = val.relevants[pred].count(item2) > 0
#         res = res1 and res2
#         if res == False:
#             return False
#     return True

# def every2(vals, pred, items, refs):
#     for val in vals:
#         res_arr = []
#         for item in items:           
#             res = val.relevants[pred].count(item) > 0
#             res_arr.append(res)
#         res = res_arr[0]
#         for i in range(len(refs)):
#             ref = refs[i]
#             res = (res and res_arr[i+1]) if ref == 'and' else (res or res_arr[i+1])
#         if res == False:
#             return False
#     return True


# list2 = [neureCtr1, neureCtr2, neureCtr3]
# item1 = ('', '', '博士')
# item2 = ('', '', '教授')
# res = every(list2, '是', item1, item2)
# res = every2(list2, '是', [item1, item2], ['and'])
# print(res)

#----------------------------------------------------

#-------------------------#所有人都呼吸---------------------------
# (∀x)(F(x)→G(x))
neureCtr1 = NeureCtr('小明')
neureCtr1.relevants = ['是', ('', '', '人')]
neureCtr1.relevants = ['呼吸', ('', '', '')]

neureCtr2 = NeureCtr('陈霞')
neureCtr2.relevants = ['是', ('', '', '人')]
neureCtr2.relevants = ['呼吸', ('', '', '')]

neureCtr3 = NeureCtr('丽莎')
neureCtr3.relevants = ['是', ('', '', '人')]
neureCtr3.relevants = ['呼吸', ('', '', '')]

neureCtr4 = NeureCtr('苏格拉底')
neureCtr4.relevants = ['是', ('', '', '人')]
# neureCtr4.relevants = ['呼吸', ('', '', '')]

list2 = [neureCtr1, neureCtr2, neureCtr3]
condition = ['是', ('', '', '人')]
target = ['呼吸', ('', '', '')]

def every(vals, condition, target):
    for val in vals:
        cond = val.relevants[condition[0]] if condition[0] in val.relevants else None
        tar = val.relevants[target[0]] if target[0] in val.relevants else None
        if cond and cond.count(condition[1]) > 0:
            res = tar.count(target[1]) > 0 if tar else False
            if res == False:
                return False
    return True

# res = every([neureCtr1, neureCtr2, neureCtr3], condition, target)
# print(res)

#苏格拉底是人，所以苏格拉底呼吸
# (∀x)(F(x)→G(x))∧F(s)→G(s)
def inference(vals, condition, target, obj):
    res = every(vals, condition, target)
    cond = obj.relevants[condition[0]] if condition[0] in obj.relevants else None
    tar = obj.relevants[target[0]] if target[0] in obj.relevants else None
    if res and cond and cond.count(condition[1]) > 0:
        if tar is None:
            obj.relevants = target
        else:
            if tar.count(target[1]) == 0:
                obj.relevants = target
        return True
    return False

# res = inference([neureCtr1, neureCtr2, neureCtr3], condition, target, neureCtr4)
# print(res)

#----------------------------------------------------
# (ヨx)(A(x)∧B(x)) => (ヨx)A(x)∧(ヨx)B(x)
# [[('some', 'x'), (('A', 'x'), 'and', ('B', 'x'))]]
# =>
# [[('some', 'x'), (('A', 'x'))], 'and', [('some', 'x'), (('B', 'x'))]]

# (∀x)F(x)∨┓ヨxG(x)
# [[('every', 'x'), (('F', 'x'))], 'or', [('not', 'some', 'x'), (('G', 'x'))]]
# =>换名规则
# (∀x)F(x)∨┓ヨyG(y)
# [[('every', 'x'), (('F', 'x'))], 'or', [('not', 'some', 'y'), (('G', 'y'))]]
# =>量词否定等价式
# (∀x)F(x)∨∀y┓G(y)
# [[('every', 'x'), (('F', 'x'))], 'or', [('every', 'y'), (('not', 'G', 'y'))]]
# =>量词辖域扩张等价式
# (∀x)(F(x)∨∀y┓G(y))
# [[('every', 'x'), (('F', 'x'), 'or', (('every', 'y'), (('not', 'G', 'y'))))]]
# =>量词辖域扩张等价式
# (∀x∀y)(F(x)∨┓G(y))
# [[('every', 'x', 'every', 'y'), (('F', 'x'), 'or', ('not', 'G', 'y'))]]
#----------------------------------------------------

# [[('every', 'x'), (('F', 'x'))], 'or', [('every', 'y'), (('G', 'y'))]]
def inference_front(info):
    item1, rel, item2 = info[0], info[1], info[2]
    if rel != 'arrow':
        res1 = item1[0] + item2[0]
        res2 = (item1[1], rel, item2[1])
    else:
        it = list(item1[0])
        it[0] = 'every' if it[0] == 'some' else 'some'
        res1 = tuple(it) + item2[0]
        res2 = (item1[1], rel, item2[1])
    res = [[res1, res2]]
    return res
# res = inference_front([[('every', 'x'), (('F', 'x'))], 'or', [('every', 'y'), (('G', 'y'))]])
# print(res)
# res = inference_front([[('every', 'x'), (('F', 'x'))], 'arrow', [('every', 'y'), (('G', 'y'))]])
# print(res)

#----------------------------------------------------
# [('not', 'some', 'y'), (('G', 'y'))]
# def inference_negative(item):
    # sub1, sub2 = item
    # if sub1

#----------------------------------------------------
# ∀x(A(x)→B)
# ∀x(┓A(x)∨B)
# [[('every', 'x'), (('A', 'x'), 'arrow', ('B'))]]
# =>
# [('every', 'x'), (('not', 'A', 'x'), 'or', ('B'))]

def replace_arrow_with_or(item):
    sub1, sub2 = item
    sub21,sub22,sub23 = sub2
    if sub22 == 'arrow':
        if sub21[0] == 'not':
            sub21 = sub21[1:]
            sub22 = 'or'
        else:
            sub21 = ('not',) + sub21
            sub22 = 'or'
    return [sub1, (sub21,sub22,sub23)]
# res = replace_arrow_with_or([('every', 'x'), (('A', 'x'), 'arrow', ('B'))])
# print(res)

#----------------------------------------------------
# (('A'), 'and', ('True'))  <=>  (('A'))
# (('True'), 'and', ('B'))  <=>  (('B'))

#----------------------------------------------------
# 所有人都呼吸      ∀x(A(x)→B(x))
neureCtr1 = NeureCtr('人')
neureCtr1.relevants = ['呼吸', ('', '所有', '')]

[[('every', 'x'), (('A', 'x'), 'arrow', ('B', 'x'))]]

def trans_to_prep(neureCtr, subject, pred):
    if neureCtr.uuid == subject:
        relevant = neureCtr.relevants['pred'][0]
        att = relevant[1]
        if att == '所有':
            val1 = ('every', 'x')
            val2 = (('A', 'x'), 'arrow', ('B', 'x'))
            return [[val1, val2]]
    return None

#-------------------------在北京打工的部分是外地人---------------------------
# A(x):x在北京打工
# B(x):x是外地人
# ヨx:部分
# 在北京打工的部分是外地人: ヨx(A(x)∧B(x))
# [[('some', 'x'), (('A', 'x'), 'and', ('B', 'x'))]]

# from typing import Sequence
# from ltp import LTP
# ltp = LTP()

# sentence = '学术委员会的每个成员都是博士并且是教授。'
# sentence = '小明、小霞，和小刘是三兄弟。'
# sentence = '他因为酒驾被交警拘留了。'
# sentence = '我们不要空话，而要行动。'
# sentence = '不是所有人都是长头发。'
# sentence = '有的水生动物是肺呼吸的'

# sentence = '肺呼吸的'
# sentence = '所有人都是长头发。'
# sentence = '所有人都'
# sentence = '一切自然数有大于它的自然数'
# sentence = '每人都有一个父亲'
# sentence = '并非所有人都是长头发。'
# sentence = '我的父亲是木材厂的会计，母亲是天台人民医院的医生。'
# sentence = '并非所有人都长头发。'
# sentence = '这个房间住着小红、小兰和他们的母亲。'
# sentence = '任何整数不是奇数就是偶数'
# sentence = 'x1不是奇数就是偶数'
# sentence = '我们不要美元，而要人名币。'
# sentence = '整天不是吃饭就是睡觉,活得真像一头猪。'
# sentence = '整天睡觉,活得真像一头猪。'
# sentence = 'x要人名币。'
# sentence = '一切动物和植物都是生物。'
# sentence = '美丽的小猪和优雅的小熊，是一对好朋友。'
# sentence = '任意的整数和任意的浮点数的乘积是浮点数。'
# sentence = '并非x0都是偶数。'
# sentence = '并非每个自然数都是偶数。'

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

# a = [(1, [(2, (3, 4)), (2, (3, 4))]), (10, [(20, (30, 40)), (20, (30, 40))])]
# b = []

# def re(a):
#     x = type(a)
#     if x == list:
#         print('list')
#     elif x == tuple:
#         print('tuple')
#     else:
#         print('else')
# re(1)

# def recuTran(val, setval):
#     t = type(val)
#     if t == list or t == tuple:
#         for a in val:
#             subt = type(a)
#             if subt == list or subt == tuple:
#                 setval.append([])
#                 recuTran(a, setval[-1])
#             else:
#                 setval.append('h')

# def func1(list):
#     a = (1,2,3)
#     t = type(list)
#     print(a)
#     print(t(a))

# recuTran(a, b)
# print(a)
# print(b)

# dic = {
#     'subject': 1,
#     'object': 22
# }
# for val in dic.items():
#     print(val)

# t = type(12)
# if t == int:
#     print('int')
# else:
#     print('else')

# a = [{'adv': '都', 'pob': None}]
# b = filter(lambda a: a['adv'].find('都') > -1, a)
# print(b)

# a = [1,2,3,4]
# print(a[:1])

# a = ['所有', [('ATT', 'subject'), ('ATT', 'object')], 'every']
# b = ('ATT', 'subject')
# print(b in a[1])

# a = [7, 6]
# a.sort()
# print(a)

# a = [('不', '是', 'ADV')]
# b,c,d = '不', '是', 'ADV'
# print((b,c,d) in a)

# a = ('不', '是', 'ADV')
# print('是' in a)

# v = ['d', 'd', 'v', 'v', 'd', 'v', 'wp', 'v', 'u', 'd', 'v', 'm', 'q', 'n', 'wp']
# wps = []
# for i in range(len(v)):
#     if v[i] == 'wp':
#         wps.append(i)
# print(wps)
# v = list('整天睡觉,活得真像一头猪。')
# print(v)

# val0 = (1,2,3)
# val1 = val0[1:]
# print(val1)

# val0 = 'A是偶数。'
# print(val0.lower())

# val0 = (1,2,3)
# val1 = (1,2,3)
# print(val0 == val1)
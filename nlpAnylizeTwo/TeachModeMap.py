# def 每一位是(content, func):
#     for i in list(content):
#         if not func(i):
#             return False
#     return True
# def 首位是(content, func):
#     if not func(content[0]):
#         return False
#     return True
# def 末位是(content, func):
#     if not func(content[-1]):
#         return False
#     return True

# # 左小括号的数量 = str.count('(')
# # def 数量(content, att):
# #     return content.count(subs)
# # ('左小括号', '数量', 'ATT') == content.count(getItem('左小括号').members[0])

# # 等于
# # def 等于(arg1, arg2):
# #     return arg1 == arg2

# def 每一位(content, obj, func):
#     length = len(content)
#     count = 0
#     for i in list(content):
#         if func(i, obj):
#             count += 1
#     return length == count
# def 是(arg1, arg2):
#     return arg2.bMember(arg1)

# # 每一位是 == 每一位(content, 是, arg2)

# # from inspect import signature

# # sig = signature(末位是)
# # print(dict(sig.parameters).keys())


# a = '0123456'
# print(a[1:3])
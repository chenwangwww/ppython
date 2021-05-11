class ClsCreater(object):
    def __init__(self, name = ''):
        self._members = []
        self._mode = []
        self._name = name
        self._action = None     

    @property
    def name(self):
        return self._name

    @property
    def action(self):
        return self._action
    @action.setter
    def action(self, value):
        self._action = value

    @property
    def members(self):
        return self._members

    def bMember(self, val):
        return str(val) in self._members
    
    def pushMember(self, val):
        if str(val) not in self._members:
            self._members.append(str(val))

    @property
    def mode(self):
        return self._mode

    def setMode(self, valArr):
        self._mode = valArr

    def bCls(self, sentence, start, modeAction, getItem):
        length = len(sentence)
        if start >= length:
            return None
        count = 0
        for i in range(start+1, length+1):
            substr = sentence[start:i]
            res1 = self.bMember(substr)
            if res1:
                count = i - start
                continue
            else:
                lenMode = len(self._mode)
                if lenMode > 0:
                    countMode = 0
                    for f in self._mode:
                        ff = modeAction(f[0]) 
                        target = getItem(f[1])                  
                        if ff(substr, target.bMember) == True:
                            countMode += 1
                    if countMode == lenMode:
                        count = i - start
                        continue
        print(count)
        return count
            

# --------------------------------------------

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

# # 整数的每一位都是整数
# def func1(str, bInt = intCls.bMember):
#     length = len(str)
#     for i in range(length):
#         if not bInt(str[i]):
#             return False
#     return True

# intCls.setMode([func1])
# # intCls.bCls('123#@4', 0)

# leftLittleBracket = ClsCreater()
# leftLittleBracket.pushMember('(')
# # leftLittleBracket.bCls('(12', 0)

# rightLittleBracket = ClsCreater()
# rightLittleBracket.pushMember(')')
# # rightLittleBracket.bCls(')12', 0)

# # 小括号的首位是左小括号
# def func2(str, bLeftLittleBracket = leftLittleBracket.bMember):
#     res = bLeftLittleBracket(str[0])
#     return res

# # 小括号的末位是右小括号
# def func3(str, bRightLittleBracket = rightLittleBracket.bMember):
#     res = bRightLittleBracket(str[-1])
#     return res

# # 左小括号的数量等于右小括号的数量
# def func4(str, leftLittleBracket = leftLittleBracket, rightLittleBracket = rightLittleBracket):
#     countl = str.count(leftLittleBracket.members()[0])
#     countr = str.count(rightLittleBracket.members()[0])
#     return countl == countr

# bracket = ClsCreater()
# bracket.pushMember('(')
# bracket.pushMember(')')
# bracket.setMode([func2, func3, func4])
# bracket.bCls('((1+2))12', 0)

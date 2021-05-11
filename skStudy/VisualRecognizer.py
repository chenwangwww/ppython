import re


class VisualRecognizer(object):
    def __init__(self):
        pass

    def recognize(self):
        pass

    # 识别小括号
    def recognize2(self, sent, pattern):
        it = re.finditer(pattern, sent)
        for match in it:
            print(match.group())
            print(match.span())
            se = self.insertBackslash(match.group())
            pattern = r'([(])[0-9\+\-\*\/]*' + se + r'[0-9\+\-\*\/]*([)])'
            self.recognize2(sent, pattern)

    # 识别加减乘除、识别整数
    def recognize3(self, sent, pattern):
        it = re.finditer(pattern, sent)
        for match in it:
            print(match.group())
            print(match.span())



    def insertBackslash(self, sent):
        sent = sent.replace('(', '\(')
        sent = sent.replace(')', '\)')
        sent = sent.replace('+', '\+')
        sent = sent.replace('-', '\-')
        sent = sent.replace('*', '\*')
        sent = sent.replace('/', '\/')
        return sent

visualRecognizer = VisualRecognizer()
# visualRecognizer.recognize()
# visualRecognizer.recognize2('(5-(1+3))+(2*4)', r'([(])([0-9\+\-\*\/]*)([)])')
# visualRecognizer.recognize3('(5-(1+3))+((2*4))', r'([0-9\)]+)([\+\-\*\/])([0-9\(])')
# visualRecognizer.recognize3('(5-(132+3))+((2*4))', r'([0-9]+)')
# visualRecognizer.recognize3('5-(132+3))+((2*4))', r'(^[\()]).*([\)]$)')

# 这个小括号里有什么？
# 1：这个是小括号吗？     2：定位到小括号里。     3：取出小括号里的内容。  

def boolFunc(sent, pattern):
    it = re.finditer(pattern, sent)
    print(len(list(it)) > 0)

def contentFunc(sent, pattern):
    it = re.finditer(pattern, sent)
    for match in it:
        print(match.groups())
        print(match.span())

def jisuanFunc(sent, pattern, res, reverse = False):
    lis = re.findall(pattern, sent)
    if len(lis) == 0:
        # print(sent)
        res.append(sent)
        return 
    if reverse:
        item = lis[-1]
        index = sent.rfind(item)
        sent = sent[:index] + str(eval(item)) + sent[index+len(item):]
        jisuanFunc(sent, pattern, res, reverse)
    else:
        item = lis[0]
        index = sent.find(item)
        sent = sent[:index] + str(eval(item)) + sent[index+len(item):]
        jisuanFunc(sent, pattern, res, reverse)

    # searchObj = re.search(pattern, sent)
    # if searchObj is not None:
    #     sent = sent[:searchObj.start()] + str(eval(searchObj.group(1))) + sent[searchObj.end():]
    #     jisuanFunc(sent, pattern)
    # else:
    #     print(sent)


# 是小括号吗('(5-(132+3))+((2*4))', r'(^[\(]).*([\)]$)')
# 小括号里('(5-(132+3))+((2*4))', r'^[\(].*[\)]$')
# 小括号里('(5-(132+3))+((2*4))', r'^[\(](.*)[\)]$')

regexMapper = {
    '小括号': r'^[\(].*[\)]$',
    '小括号里': r'([(][0-9\+\-\*\/]*[)])',
    '乘法': r'([0-9]+\*[0-9]+)',
    '乘法和除法': r'([0-9]+[\*\/][0-9]+)',
    '加法和减法': r'([0-9]+[\+\-][0-9]+)',
}

funcMapper = {
    '有什么': 'contentFunc',
    r'是.*吗': 'boolFunc',
    '计算': 'jisuanFunc',
}

propsMapper = {
    '从左往右': {'reverse': False},
    '从右往左': {'reverse': True},
}

def sentToSpecificMap(sent, mapper, greedy = False):
    items = mapper.items()
    res = None
    for item in items:
        it = re.finditer(item[0], sent)
        if len(list(it)) > 0:
            if greedy:
                res = res if res is not None and len(res[0]) >= len(item[0]) else item
            else:
                res = item
                break
    return res

def sentToMap(sent, target):
    funcItem = sentToSpecificMap(sent, funcMapper)
    regexItem = sentToSpecificMap(sent, regexMapper, greedy=True)
    func = eval(funcItem[1])
    res = []
    func(target, regexItem[1], res)
    res = res[0] if len(res) > 0 else None
    return res

def flowMgr(target, config):
    for conf in config:
        target = sentToMap(conf, target)
    print(target)

# sentToMap('是小括号吗', '(1+3+5-6)')
# sentToMap('小括号里有什么', '(1+3+5-6)')
# sentToMap('计算小括号里的内容', '(5-(1+3))+(2*4)')
# sentToMap('计算乘法', '(5-(1+3))+(2*4)')

# 计算小括号里的内容
# 从左往右，计算乘法和除法
# 从左往右，计算加法和减法

flowMgr('(5-(1+3)+2)*4/3', ['计算小括号里的内容', '从左往右，计算乘法和除法', '从左往右，计算加法和减法'])

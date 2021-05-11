import re

pattern = re.compile(r'\d+')

def abstMath(source, dest, pattern):
    if source == '':
        return
    m = pattern.match(source)
    if m is None:
        dest.append(source[0])
        source = source[1:]
        abstMath(source, dest, pattern)
    else:
        val = m.group(0)
        dest.append(val)
        source = source[len(val):]
        abstMath(source, dest, pattern)

dest = []

def pairCharsOne(left, right):
    vall = []
    for i in range(len(dest)):
        if dest[i] == left:
            vall.append(i)
        elif dest[i] == right:
            break
    return vall

def pairCharsTwo(leftList, right):
    lens = len(leftList)
    valr = []
    count = 0
    for i in range(len(dest)):
        if dest[i] == right and count < lens:
            valr.append(i)
            count += 1
    return valr

def pairCharsThree(leftList, rightList):
    lens = len(leftList)
    val = []
    for i in range(len(leftList)):
        r = ''.join(dest[leftList[i]:rightList[-i-1]+1])
        val.append(r)
    return val

resPair = []
def pairChars(sentence):
    global dest
    dest = []
    abstMath(sentence, dest, pattern)
    leftList = pairCharsOne('(', ')')
    rightList = pairCharsTwo(leftList, ')')
    res = pairCharsThree(leftList, rightList)
    res.reverse()
    if len(res) > 0:
        resPair.append(res)
        sentence = sentence[rightList[-1]+1:]
        pairChars(sentence)
    
sentence = '(5-(4-3))/((5-3)*2)'
pairChars(sentence)
# pairChars('(5-3)')

# print(resPair)

def replacePair(sentence):
    for i in range(len(resPair)):
        old = resPair[i][-1]
        sentence = sentence.replace(old, 'a'*len(old))
    return sentence

rep = replacePair(sentence)
def operationOrder():
    pattern2 = re.compile(r'\w+')
    dest2 = []
    abstMath(rep, dest2, pattern2)
    valS = []
    valF = []
    for i in range(len(dest2)):
        if dest2[i] == '*' or dest2[i] == '/':
            valS.append(i)
        elif dest2[i] == '+' or dest2[i] == '-':
            valF.append(i)
    print([valS, valF])

operationOrder()
print(eval('(2+3)'))
def action_左边(content, symbolIndex):
    return content[:symbolIndex]

def action_右边(content, symbolIndex):
    return content[symbolIndex+1:]

def action_里面(content, startIndex, endIndex):
    return content[startIndex + 1: endIndex]

def action_外面(content, outIndex1, outIndex2):
    res2 = content[outIndex2 + 1:] if outIndex2 < (len(content) - 1) else None
    return content[:outIndex1], res2

def action_数量(content, ATT, getItem):
    item = getItem(ATT)
    count = 0
    for val in item.members:
        count += content.count(val)   
    return count
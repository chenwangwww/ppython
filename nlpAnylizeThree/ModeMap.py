def 是(subj, obj, getItem):
    objIns = getItem(obj)
    res = objIns.bMember(subj)
    return res

def 整数(content, getItem):
    item = getItem('整数')
    for i in content:
        if not item.bMember(i):
            return False
    return True

def 等于(subjRes, objRes):
    return subjRes == objRes
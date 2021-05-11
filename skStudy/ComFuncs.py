def findCW(keyStr, array):
    res = None
    for i in array:
        if i.find(keyStr) > -1:
            res = i
    return res
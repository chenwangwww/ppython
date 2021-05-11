def teach_是(subj, obj, getItem):
    subjIns = getItem(subj)
    objIns = getItem(obj)
    subjIns.pushRelevant(obj)
    subjIns.pushMember(subj)
    objIns.pushMember(subj)
    return subjIns, objIns
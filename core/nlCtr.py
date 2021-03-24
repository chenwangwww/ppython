from ltp import LTP
ltp = LTP()

class NlCtr:
    def __init__(self):
        self.word_path = './assets/words.txt'
        self.inte_pron_list = self.get_inte_prons()

    def get_inte_prons(self):
        with open(self.word_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        list = eval(lines[0])
        return list

    def b_specific_question(self, sentence):
        seg, hidden = ltp.seg([sentence])
        srl = ltp.srl(hidden, keep_empty=False)
        item = srl[0][0] if len(srl[0]) > 0 else None
        if item and item[1][0][0] == 'A0' and item[1][1][0] == 'A1':
            target_tuple = item[1][1]
            target = ''.join(seg[0][target_tuple[1]:target_tuple[2]+1])
            for val in self.inte_pron_list:
                if val in target:
                    return True
        return False

    def get_content_and_pred(self, sentence):
        seg, hidden = ltp.seg([sentence])
        srl = ltp.srl(hidden, keep_empty=False)
        
        item = srl[0][0] if len(srl[0]) > 0 else None
        if item and item[1][0][0] == 'A0' and item[1][1][0] == 'A1':
            content_tuple = item[1][0]
            content = ''.join(seg[0][content_tuple[1]:content_tuple[2]+1])
            predicate = seg[0][item[0]]

            seg2, hidden2 = ltp.seg([content])
            dep2 = ltp.dep(hidden2)
            if len(dep2[0]) > 1:
                content = seg2[0][0]
                predicate = ''.join(seg2[0][2:])
            return [content, predicate]
        return None

nlctr = NlCtr()
res = nlctr.get_content_and_pred('故宫的官方电话是多少？')
print(res)
res2 = nlctr.b_specific_question('故宫的官方电话是15824034444。')
print(res2)
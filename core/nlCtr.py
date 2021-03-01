class NlCtr:
    def __init__(self):
        self.word_path = './assets/words.txt'
        
    def read_words(self):
        with open(self.word_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        arr = eval(lines[0])
        print(arr)
        print(type(arr))


# from ltp import LTP
# ltp = LTP()

# seg,hidden = ltp.seg(['双子叶植物'])
# srl = ltp.srl(hidden, keep_empty=False)
# pos = ltp.pos(hidden)
# print(seg)
# print(pos)
# print(srl)
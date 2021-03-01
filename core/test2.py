import pickle
import codecs
from NeureCtr import NeureCtr
neureCtr = NeureCtr(100)
neureCtr.relevants = [(19, 0, 0), 0]
neureCtr.relevants = [(19, 0, 1), 1]
neureCtr.relevants = [(19, 0, 2), 2]
res = pickle.dumps(neureCtr)
print(res)
print('------------')
s = str(res)
print(s)
print('-----------------')
s2 = s[2:-1]
print(s2)
print('-----------------')
s3 = s2.encode()
print(s3)
print('-----------------')
s4 = codecs.escape_decode(s3, "hex-escape")
print(s4)
print('-----------------')
print(s4[0] == res)
class Prop:
    def __init__(self, name):
        self._name = name
        self._prop = lambda a,b:(a[0], a[1], b[2])

iss = Prop('是')
print(iss._prop(('是', '正方形', '长方形'), ('是', '长方形', '四边形')))

#传递性

#限定性
#一个国家的首都只有一个，中国是一个国家，所以中国的首都只有一个

# ('只有', '一个国家的首都', '一个')  ('是', '中国', '一个国家')  ('只有', '中国的首都', '一个')

# 黑的反义词是白 多的反义词是少

# 反义词{
#     （‘是’，‘黑’，‘白’）
#     （‘是’，‘多’，‘少’）
# }

# 首都{
#     （‘只有’，‘国家’，‘一个’）
#     （‘是’，‘中国’，‘北京’）
#     （‘是’，‘美国’，‘纽约’）
# }

# 苹果是红色的
# 苹果{
#     （‘是’，‘’，‘红色’）
# }

#所有的人都呼吸
# 人{
#     ‘呼吸’: [(‘所有’， ‘’）]
# }
# def M(x):
#     if x is 人:
#         x{
#             ‘呼吸’:[(‘’，‘’）]
#         } 
# 任意x（x是人 and x呼吸）

# 小明是人
# 小明{
#     ‘是’:[(‘’，‘人’）]
#     ‘呼吸’:[(‘’，‘’）]
# }

# 有的人不呼吸
# 人{‘呼吸’：[（‘not’，‘有的’， ‘’）] }
# 存在x（x是人 and x不呼吸）

# 有些人是左撇子
# 人{
#     ‘是’：[(‘有些’，‘左撇子’)]
# }
# def D(x):
#     res = 人.filter((val){val is 左撇子})
#     return res.find(x) > -1

# x是人，人都是要死的
# def M(x):
#     if x is 人:
#         x is 要死的
# x是苏格拉底，苏格拉底是人
# def D(x):
#     if x is 苏格拉底:
#         x is 人

# x是苏格拉底，苏格拉底是要死的
# def C(x):
#     if x is 苏格拉底:
#         x is 要死的

#--------------------------------
# subject{
#     'pred':[('否定词','主语的定语'，'宾语结构')]
# }
# 宾语结构：（‘宾语的定语’，‘宾语’，‘ATT’）
#--------------------------------
#       条件           结论
# ([x is 苏格拉底],   [x is 人])
# ([x is 人],         [x is 要死的, x is 呼吸])
#--------------------------------
# x is 苏格拉底 -> x is 人 -> x is 要死的, x is 呼吸
# x is 苏格拉底 -> x is not 呼吸 (与 ‘x is 呼吸’冲突，真值为零)
#--------------------------------

# 在码头上，人们在忙着卸货。
# 小明和小红都是他的孩子。ATT
# 小明{
#     （‘是’，‘’，（‘他’，‘孩子’，‘ATT’））
# }
# 小红{
#     （‘是’，‘’，（‘他’，‘孩子’，‘ATT’））
# }

#是非问句
# 他是你爸爸吗？
# 你们去不去？
# 天气冷不冷？
# 我可以进来吗？（补全之后的主谓宾，例如：我进来房间）
# （小明进来房间，&&，房间里都是垃圾=》你不要进来房间） 
# ？（‘进来’，‘小明’，‘房间’） 里{（‘是’，‘房间’，‘垃圾’）}    =》 ！（‘进来’，‘小明’，‘房间’）
# （小明进来房间，&&，小明是坏人=》你不要进来房间）
# ？（‘进来’，‘小明’，‘房间’） （‘是’，‘小明’，‘坏人’）    =》 ！（‘进来’，‘小明’，‘房间’）

#正反问句
# 是不是你也想去呢？
# 现在你们听见了没有？（比如有很轻的鸟叫声，补全之后的主谓宾是：你们听见鸟叫声）

#选择问句
# 你喜欢文学，还是喜欢历史？
# 到底是你跑的快，还是他跑得快？

#反问句
# 难道他想失败吗？（补全之后的主谓宾是：他想失败）
# 用了人家的东西，不告诉他怎么行？（补全之后的主谓宾，例如：你告诉他）



#我打量了他一眼。

#这里风景优美。这里的风景是优美的。风景{（‘是’，‘这里’，‘优美’）}
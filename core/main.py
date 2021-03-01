import pickle
import crawler
from Datactr import DataCtr
from NeureCtr import NeureCtr
from DbCtr import ctr
# from ltp import LTP
# ltp = LTP()

TBNAME = "chen_info"

def getItem(id):
    item = None
    query = ctr.queryData(TBNAME, id)
    if query:
        item = pickle.loads(query[1])
    else:
        item = NeureCtr(id)
    return item

def smartUpDb(item):
    query = ctr.queryData(TBNAME, item.uuid)
    if query:
        ctr.updateData(TBNAME, item.uuid, pickle.dumps(item))
    else:
        ctr.insertData(TBNAME, {'id':item.uuid, 'sequence':pickle.dumps(item)})


datactr = DataCtr()
# datactr.insert_txt('明明网络')
# datactr.create_envir_txt()
# print(datactr.get_txt_from_label(26, 'envir'))

# crawler.crawl_geo_search('故宫')
# for info in crawler.info_arr:
#     res = datactr.web_info_teach(info)
#     print(res)

# print(datactr.label_list_to_text([(19, 0, 0), 0]))
# print(datactr.label_list_to_text([(19, 0, 1), 1]))
# print(datactr.label_list_to_text([(19, 0, 2), 2]))



def saveSeq(name):
    crawler.crawl_geo_search(name)
    print(name)
    neureCtr = None
    a = None
    print(crawler.info_arr)
    for info in crawler.info_arr:
        res = datactr.web_info_teach(info)
        if neureCtr is None:
            print('****************')
            neureCtr = NeureCtr(res[0][1])
            a = res
        neureCtr.relevants = res
    print(a)
    print(neureCtr.uuid)
    print(neureCtr.relevants)
    smartUpDb(neureCtr)
    print(str(datactr.label_list_to_text(a)))
    return str(datactr.label_list_to_text(a))
    

# saveSeq('西湖')
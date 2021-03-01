class DataCtr:
    def __init__(self):
        self.target_path = '/usr/local/src/ppython/assets/target.txt'
        self.pred_path = '/usr/local/src/ppython/assets/pred.txt'
        self.content_path = '/usr/local/src/ppython/assets/content.txt'
        self.envir_path = '/usr/local/src/ppython/assets/envir.txt'
        self.dict_path = '/usr/local/src/ppython/assets/dict_txt.txt'
        self.dict_txt = self.get_dict_txt(self.dict_path)
        self.content_data = self.get_dict_txt(self.content_path)
        self.target_data = self.get_dict_txt(self.target_path)
        self.pred_data = self.get_dict_txt(self.pred_path)
        self.envir_data = self.get_txt_from_envir()

    #读取文本内容并转成字典
    def get_dict_txt(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        dict_txt = eval(lines[0]) if len(lines) > 0 else {}
        return dict_txt

    def create_content_txt(self, content):
        return self.create_dict_txt(content, self.content_path, self.content_data)

    def create_predicate_txt(self, predicate):
        return self.create_dict_txt(predicate, self.pred_path, self.pred_data)

    def create_target_txt(self, target):
        return self.create_dict_txt(target, self.target_path, self.target_data)

    def create_dict_txt(self, text, path, dict_txt):
        data = self.get_number_tuple(text)
        if data not in dict_txt:
            dict_txt.update({data: len(dict_txt)})
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(dict_txt))
        return dict_txt[data]

    #从汉字-数字对照表dict_txt.txt中获取数字元组
    def get_number_tuple(self, txt):
        list_data = []
        for s in txt:
            list_data.append(self.dict_txt[s])
        return tuple(list_data)
    
    def insert_txt(self, txt):
        txt_temp = ''
        self.dict_txt = self.get_dict_txt(self.dict_path)
        for s in txt:
            if s not in self.dict_txt:
                txt_temp += s
        txt_temp = ''.join(set(txt_temp))
        count = len(self.dict_txt)
        for s in txt_temp:
            self.dict_txt[s] = count
            count += 1
        with open(self.dict_path, 'w', encoding='utf-8') as f:
            f.write(str(self.dict_txt))

    def create_envir_txt(self):
        with open(self.envir_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        names = eval(lines[0])
        actions = eval(lines[1])

        for name in names:
            self.insert_txt(name)
        for action in actions:
            self.insert_txt(action)

        list_envir = []
        count = 0
        for name in names:
            for action in actions:
                for name2 in names:
                    title = name.strip() + action.strip() + name2.strip()
                    data = self.get_number_tuple(title)
                    list_envir.append([data, count])
                    count += 1
        with open(self.envir_path, 'w', encoding='utf-8') as f:
            f.writelines([str(names), '\n', str(actions), '\n', str(dict(list_envir))])
        self.envir_data = self.get_txt_from_envir()

    def get_txt_from_envir(self):
        with open(self.envir_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        envir_data = eval(lines[2])
        return envir_data

    #字典的键、值互换
    def swap_key_value(self, dic):
        keys, values = list(dic.keys()), list(dic.values())
        temp = {}
        for i in range(len(keys)):
            temp.update({values[i]: keys[i]})
        return temp

    #根据数字元组获取对应汉字
    def get_txt_from_tuple(self, data):
        temp = ''
        dic = self.swap_key_value(self.dict_txt)
        for i in data:
            temp += dic[i]
        return temp

    def get_txt_from_label(self, label, flag):
        dic = None
        if flag == 'envir':
            dic = self.envir_data
        elif flag == 'content':
            dic = self.content_data
        elif flag == 'pred':
            dic = self.pred_data
        elif flag == 'target':
            dic = self.target_data

        if dic is None:
            raise Exception('键名错误')
        data = self.swap_key_value(dic)
        tup = data[label]
        res = self.get_txt_from_tuple(tup)
        return res

    def web_info_teach(self, info):
        for val in info.values():
            self.insert_txt(val)
        envir_label = self.envir_data[self.get_number_tuple(info['envir'])]
        content_label = self.create_content_txt(info['content'])
        pred_label = self.create_predicate_txt(info['pred'])
        target_label = self.create_target_txt(info['target'])
        return [(envir_label, content_label, pred_label), target_label]

    def label_list_to_text(self, data):
        target = self.get_txt_from_label(data[1], 'target')
        pred = self.get_txt_from_label(data[0][2], 'pred')
        content = self.get_txt_from_label(data[0][1], 'content')
        envir = self.get_txt_from_label(data[0][0], 'envir')
        info = {'content': content, 'target': target, 'pred': pred, 'envir': envir}
        return info

    def relevants_to_text(self, relevants):
        txt = []
        for key, values in relevants.items():
            pred = self.get_txt_from_label(key[0][2], 'pred')
            content = self.get_txt_from_label(key[0][1], 'content')
            envir = self.get_txt_from_label(key[0][0], 'envir')
            targets = []
            for val in values:
                targets.append(self.get_txt_from_label(val, 'target'))
            txt.append({'content': content, 'target': targets, 'pred': pred, 'envir': envir})
        return txt
import re

# it = re.search(r'(\w+):\/\/([^/:]+)(:\d*)?([^# ]*)', 'http://www.runoob.com:80/html/html-tutorial.html')
# print(it.groups())
# print(it.span())

# it = re.finditer(r'\b([a-z]+) \1\b', 'Is is the cost of of gasoline going up up', re.I)
# for item in it:
#     print(item.group())
#     print(item.span())

# lines = '''
# run
# run
# '''
# it = re.finditer(r'^run', lines, re.I|re.M)
# for item in it:
#     print(item.group())
#     print(item.span())

# line = '陈望'
# enc = line.encode('utf-8')
# print(enc)

# char = '0'
# enc = ord(char)
# ch = chr(enc)
# print(enc)
# print(ch)

# string = '青菜'
# for c in string:
#     print(ord(c))

# from sklearn import svm, datasets

# iris = datasets.load_iris()
# print(iris.data)

# import os
# def file_name(file_dir):
#     for root, dirs, files in os.walk(file_dir):
#         print(root)
#         print(dirs)
#         print(files)
#         print('----------------------')
# file_name(r'D:\study\nlpstudy\ppython\regexStudy')

# dirs = os.listdir(r'./regexStudy/models')
# for file in dirs:
#     print(file)

# root = r'D:\study\nlpstudy\ppython\regexStudy'
# file_names = [os.path.join(path, name) for path, subdirs, files in os.walk(root) for name in files]
# print(file_names)

# import tensorflow as tf

# mnist = tf.keras.datasets.mnist
# (x_train, y_train), (x_test, y_test) = mnist.load_data()
# x_train, x_test = x_train / 255.0, x_test / 255.0
# model = tf.keras.models.Sequential([
#     tf.keras.layers.Flatten(input_shape=(28, 28)),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dropout(0.2),
#     tf.keras.layers.Dense(10, activation='softmax')
# ])
# model.compile(optimizer='adam',
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])
# model.fit(x_train, y_train, epochs=5)
# model.evaluate(x_test, y_test, verbose=2)

import tensorflow as tf

a = tf.placeholder('float')
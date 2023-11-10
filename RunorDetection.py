# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

'''
@article{song2018ced,
# title={CED: Credible Early Detection of Social Media Rumors},
#  author={Song, Changhe and Tu, Cunchao and Yang, Cheng and Liu, Zhiyuan and Sun, Maosong},
  journal={arXiv preprint arXiv:1811.04175},
  year={2018}
'''



import zipfile
import os
import io
import random
import json
import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# import paddle
# import paddle.fluid as fluid
# import paddle.nn as nn
# from paddle.nn import Conv2D, Linear, Embedding
# from paddle.fluid.dygraph.base import to_variable


# 解压原始数据集，将Rumor_Dataset.zip解压至data目录下
src_path = "C:/Users/杨思博/Downloads/Rumor_Dataset.zip"  # 这里填写自己项目所在的数据集路径
target_path = "C:/Users/杨思博/Desktop/Chinese_Rumor_Dataset-master"
if (not os.path.isdir(target_path)):
    z = zipfile.ZipFile(src_path, 'r')
    z.extractall(path=target_path)
    z.close()

# 分别为谣言数据、非谣言数据、全部数据的文件路径
rumor_class_dirs = os.listdir(
    os.path.join(target_path, "C:/users/杨思博/Desktop/Chinese_Rumor_Dataset-master/CED_Dataset/rumor-repost"))
# 这里填写自己项目所在的数据集路径
non_rumor_class_dirs = os.listdir(os.path.join(target_path, "C:/Users/杨思博/Desktop/Chinese_Rumor_Dataset-master/CED_Dataset/non-rumor-repost"))
original_microblog = os.path.join(target_path, "C:/Users/杨思博/Desktop/Chinese_Rumor_Dataset-master/CED_Dataset/original-microblog")

# 谣言标签为0，非谣言标签为1
rumor_label = "0"
non_rumor_label = "1"

# 分别统计谣言数据与非谣言数据的总数
rumor_num = 0
non_rumor_num = 0
all_rumor_list = []
all_non_rumor_list = []


# 解析谣言数据  all_data.txt
for rumor_class_dir in rumor_class_dirs:
    if not rumor_class_dir.endswith('.DS_Store'):
        # 遍历谣言数据，并解析
        file_path = os.path.join(original_microblog, rumor_class_dir)
        with open(file_path, 'r',encoding='utf-8') as f:
            rumor_content = f.read()
        rumor_dict = json.loads(rumor_content)
        all_rumor_list.append(rumor_label + "\t" + rumor_dict["text"] + "\n")
        rumor_num += 1
# 解析非谣言数据
for non_rumor_class_dir in non_rumor_class_dirs:
    if not non_rumor_class_dir.endswith('.DS_Store'):
        file_path = os.path.join(original_microblog, non_rumor_class_dir)
        with open(file_path, 'r',encoding='utf-8') as f2:
            non_rumor_content = f2.read()
        non_rumor_dict = json.loads(non_rumor_content)
        all_non_rumor_list.append(non_rumor_label + "\t" + non_rumor_dict["text"] + "\n")
        non_rumor_num += 1

print("谣言数据总量为：" + str(rumor_num))
print("非谣言数据总量为：" + str(non_rumor_num))

# 全部数据进行乱序后写入all_data.txt
data_list_path = "C:/Users/杨思博/Desktop/Chinese_Rumor_Dataset-master/CED_Dataset/"


all_data_path = data_list_path + "all_data.txt"
all_data_list = all_rumor_list + all_non_rumor_list

random.shuffle(all_data_list)

# 在生成all_data.txt之前，首先将其清空
with open(all_data_path, 'w',encoding='utf-8') as f:
    f.seek(0)
    f.truncate()

with open(all_data_path, 'a',encoding='utf-8') as f:
    for data in all_data_list:
        f.write(data)
print('all_data.txt已生成')


# 生成数据字典  dict.txt

def create_dict(data_path, dict_path, dict_xlsx_path):
    dict_set = set()
    # 读取全部数据
    with open(data_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # 把数据生成一个元组
    for line in lines:
        content = line.split('\t')[-1].replace('\n', '')
        for s in content:
            dict_set.add(s)
    # 把元组转换成字典，一个字对应一个数字
    dict_list = []
    i = 0
    for s in dict_set:
        dict_list.append([s, i])
        i += 1
    # 添加未知字符
    dict_txt = dict(dict_list)
    end_dict = {"<unk>": i}
    dict_txt.update(end_dict)
    # 把这些字典保存到本地中
    with open(dict_path, 'w', encoding='utf-8') as f:
        f.write(str(dict_txt))
    print("数据字典生成完成！", '\t', '字典长度为：', len(dict_list))

    # 将字典转换为DataFrame
    df = pd.DataFrame(dict_list, columns=['single word', 'times'])
    # 将DataFrame写入Excel表格
    writer = pd.ExcelWriter(dict_xlsx_path)
    df.to_excel(writer, index=False)
    writer._save()
    print("数字字典.xlsx生成完成！")

data_path = "C:/Users/杨思博/Desktop/Chinese_Rumor_Dataset-master/CED_Dataset/all_data.txt"
dict_path = "C:/Users/杨思博/Desktop/Chinese_Rumor_Dataset-master/CED_Dataset/your_dict_file.txt"
dict_xlsx_path = "C:/Users/杨思博/Desktop/Chinese_Rumor_Dataset-master/CED_Dataset/dict.xlsx"
create_dict(data_path, dict_path, dict_xlsx_path)


# 创建序列化表示的数据,并按照一定比例划分训练数据与验证数据
# 这段代码的作用是将原始数据处理成用于文本分类模型训练和评估的数据列表，最终生成了两个文件：eval_list.txt 用于评估，train_list.txt 用于训练。
def create_data_list(data_list_path):
    # 打开包含字典数据的文件，读取并解析成字典
    with open(os.path.join(data_list_path, 'dict.txt'), 'r', encoding='utf-8') as f_data:
        dict_txt = eval(f_data.readlines()[0])

    # 打开包含所有数据的文件，读取每行数据
    with open(os.path.join(data_list_path, 'all_data.txt'), 'r', encoding='utf-8') as f_data:
        lines = f_data.readlines()

    i = 0
    # 创建用于写入评估数据的文件和训练数据的文件
    with open(os.path.join(data_list_path, 'eval_list.txt'), 'a', encoding='utf-8') as f_eval, \
            open(os.path.join(data_list_path, 'train_list.txt'), 'a', encoding='utf-8') as f_train:
        # 遍历所有数据行
        for line in lines:
            # 提取文本标题和标签
            title = line.split('\t')[-1].replace('\n', '')
            lab = line.split('\t')[0]
            t_ids = ""
            # 每8行数据将用于评估，其余用于训练
            if i % 8 == 0:
                # 将标题文本转换为字典中的相应编号并拼接成字符串
                for s in title:
                    temp = str(dict_txt[s])
                    t_ids = t_ids + temp + ','
                # 去掉最后一个逗号，然后拼接标签并写入评估文件
                t_ids = t_ids[:-1] + '\t' + lab + '\n'
                f_eval.write(t_ids)
            else:
                # 同样将标题文本转换为字典中的相应编号并拼接成字符串
                for s in title:
                    temp = str(dict_txt[s])
                    t_ids = t_ids + temp + ','
                # 去掉最后一个逗号，然后拼接标签并写入训练文件
                t_ids = t_ids[:-1] + '\t' + lab + '\n'
                f_train.write(t_ids)
            i += 1

    print("数据列表生成完成！")

data_list_path = "C:/Users/杨思博/Desktop/Chinese_Rumor_Dataset-master/CED_Dataset/"
create_data_list(data_list_path)


# 这段代码定义了一个数据读取器函数 data_reader，用于从指定文件中读取数据并返回一个数据生成器函数。
# 生成器函数会逐行读取文件中的数据，将文本内容和标签解析后返回。如果指定了 shuffle 参数并且 phrase 为 "train"，则会在训练数据中对数据进行洗牌。
# 这个数据读取器可以用于加载文本分类任务的训练和评估数据。
def data_reader(file_path, phrase, shuffle=False):
    # 初始化一个空列表用于存储数据
    all_data = []

    # 打开文件并逐行读取数据
    with io.open(file_path, "r", encoding='utf8') as fin:
        for line in fin:
            # 分割每行数据，按照制表符分隔
            cols = line.strip().split("\t")
            # 如果数据列数不等于2，跳过该行数据
            if len(cols) != 2:
                continue
            # 解析标签，将第二列数据转换为整数
            label = int(cols[1])

            # 分割文本内容，将第一列数据按逗号分隔并存储为列表
            wids = cols[0].split(",")
            # 将文本内容和标签组成一个元组，添加到数据列表中
            all_data.append((wids, label))

    # 如果需要对数据进行洗牌（shuffle）
    if shuffle:
        if phrase == "train":
            random.shuffle(all_data)

    # 定义一个数据生成器函数
    def reader():
        for doc, label in all_data:
            # 生成器函数，每次迭代产生一组文本内容和标签
            yield doc, label

    # 返回数据生成器函数
    return reader

file_path = "C:/Users/杨思博/Desktop/Chinese_Rumor_Dataset-master/CED_Dataset/train_list.txt"
phrase = "train"  # 或 "eval"，表示数据集是训练集还是评估集
shuffle = True  # 是否对训练数据进行洗牌

# 调用数据读取器函数，返回一个数据生成器
data_generator = data_reader(file_path, phrase, shuffle)


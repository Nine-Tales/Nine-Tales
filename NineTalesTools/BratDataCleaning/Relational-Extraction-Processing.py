#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/18 10:12 
# @Author : Nine-Tales
# @Desc: 对brat处理好的数据进行整理, 整理成需要的json格式;

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import pandas as pd
import json

# class Relational_Extraction(object):
#
#     def __init__(self):
#         pass


def process_ann_to_json(path):

    # 读取数据, 得到[0, 1, 2]三列;
    df = pd.read_csv(path, header=None, encoding="utf-8", sep="\t")
    # 将中间[1]列分割为["type", "start", "end"]三列, 并删除[1]列;
    df["type"], df["start"], df["end"] = df[1].str.split(" ", 2).str
    df = df.drop([1], axis=1)
    # 重命名[0, 2]列
    df.rename(columns={0: "id", 2: "entity"}, inplace=True)
    # 将关系行中的"args:"干扰字符串去掉;
    for i in range(0, len(df)):
        if "R" in df["id"][i]:
            df["start"][i] = (df["start"][i].split(":"))[1]
            df["end"][i] = (df["end"][i].split(":"))[1]

    out = df.to_json(orient="records")[1:-1].replace("},{", "}\n{")
    with open("df2json.txt", "w", encoding="utf-8") as fw:
        fw.write(out)


def process_json_2_need(json_path):

    if not os.path.exists("Output"):
        os.makedirs("Output")

    with open(json_path, "r", encoding="utf-8") as fr:
        data = fr.readlines()

    relation_dict = {'text': '', 'spo_list': [{'predicate': '', 'object_type': '', 'subject_type': '',
                                               'object': '', 'subject': ''}]}

    for i in range(len(data)):
        data_dict = json.loads(data[i])

        if "R" in data_dict["id"]:
            relation_dict['spo_list'][0]['predicate'] = data_dict['type']
            for j in range(0, len(data)):
                data_j = json.loads(data[j])
                if data_j['id'] == data_dict['start']:
                    relation_dict['spo_list'][0]['object_type'] = data_j['type']
                    relation_dict['spo_list'][0]['object'] = data_j['entity']
                elif data_j['id'] == data_dict['end']:
                    relation_dict['spo_list'][0]['subject_type'] = data_j['type']
                    relation_dict['spo_list'][0]['subject'] = data_j['entity']
            with open("Output/train.json", "a+", encoding="utf-8") as fw:
                fw.write(str(relation_dict) + '\n')


def process_json_2_test_data(json_path):
    with open(json_path, "r", encoding="utf-8") as fr:
        test_data = fr.readlines()
    for i in test_data:
        data_dict = json.loads(i.strip())
        with open("Output/test.json", "a+", encoding="utf-8") as fw:
                fw.write(str({"text": data_dict["text"]}) + '\n')


def txt_2_test_data(json_path):
    with open(json_path, "r", encoding="utf-8") as fr:
        test_data = fr.readlines()

    for i in test_data:
        test_dict = {}
        if len(test_data) > 0:
            test_dict["test"] = i.strip()
        with open("test_for_json.json", "a+", encoding="utf-8") as fw:
            fw.write(str(test_dict) + "\n")


def count_text(json_path):
    with open(json_path, "r", encoding="utf-8") as fr:
        data_source = fr.readlines()

    total = len(data_source)
    use = 0
    for i in data_source:
        if len(i.strip()) > 0:
            use += 1
    percent = "%.2f"% (use / total)
    print(percent)



if __name__ == '__main__':
    # process_ann_to_json("BratData/3.ann")
    # process_json_2_need("BratData/df2json.txt")
    # process_json_2_test_data("Output/train.json")
    # txt_2_test_data("BratData/文本.txt")
    count_text("BratData/predicate_predict.txt")



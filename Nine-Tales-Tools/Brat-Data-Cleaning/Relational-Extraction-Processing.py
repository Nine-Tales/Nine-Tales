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
            for j in range(0, i):
                data_j = json.loads(data[j])
                if data_j['id'] == data_dict['start']:
                    relation_dict['spo_list'][0]['object_type'] = data_j['type']
                    relation_dict['spo_list'][0]['object'] = data_j['entity']
                if data_j['id'] == data_dict['end']:
                    relation_dict['spo_list'][0]['subject_type'] = data_j['type']
                    relation_dict['spo_list'][0]['subject'] = data_j['entity']
                    break
            with open("Output/train.json", "a+", encoding="utf-8") as fw:
                fw.write(str(relation_dict) + '\n')


if __name__ == '__main__':
    process_ann_to_json("BratData/Relation_Annotation.ann")
    process_json_2_need("BratData/df2json.txt")



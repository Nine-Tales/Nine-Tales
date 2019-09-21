#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/21 9:56 
# @Author : Nine-Tales
# @Desc: 

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import numpy as np


# Dice 系数
def dice_coefficient(a, b):
    # dice = 2nt / na + nb
    a_bigrams =set(a)
    b_bigrams = set(b)
    overlap = len(a_bigrams & b_bigrams)
    # sum([(x - y) ** p for (x, y) in zip(vec1, vec2)]) ** (1 / p)
    return overlap * 2.0 / (len(a_bigrams) + len(b_bigrams))


# 闵可夫斯基距离
def minkowski_distance(vec1, vec2, p=3):
    # 当p=1时, 为曼哈顿距离;
    # 当p=2时, 为欧氏距离;
    # 当p->∞时, 为切比雪夫距离;
    return np.linalg.norm(vec1 - vec2, ord=p)


def cosine_distance(vec1, vec2):
    # 余弦夹角
    vec1_norm = np.linalg.norm(vec1)
    vec2_norm = np.linalg.norm(vec2)
    return vec1.dot(vec2) / (vec1_norm * vec2_norm)


def hamming_distance(vec1, vec2):
    # 汉明距离
    return np.shape(np.nonzero(vec1 - vec2)[0])[0]


def jaccard_similarity_coefficient(vec1, vec2):
    # jaccard距离
    set1 = set(vec1)
    set2 = set(vec2)
    if len(set1) == 0 or len(set2) == 0:
        return 0
    return len(set1 & set2) / float(len(set1 | set2))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 135-Candy.py
# @Author: Nine-Tales
# @Date  : 2019-09-10
# @Desc  : 135-分发糖果

"""
老师想给孩子们分发糖果，有 N 个孩子站成了一条直线，老师会根据每个孩子的表现，
预先给他们评分。

你需要按照以下要求，帮助老师给这些孩子分发糖果：

每个孩子至少分配到 1 个糖果。
相邻的孩子中，评分高的孩子必须获得更多的糖果。
那么这样下来，老师至少需要准备多少颗糖果呢？
"""
def candy(ratings):
    n = len(ratings)
    tmp = [0] * n
    tmp = [i for i in range(1, n)]
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            tmp[i] = tmp[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            tmp[i] = max(tmp[i], tmp[i + 1] + 1)
    s = n + sum(tmp)
    return s

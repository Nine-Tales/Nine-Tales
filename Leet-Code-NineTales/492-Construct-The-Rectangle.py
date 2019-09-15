#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 492-Construct-The-Rectangle.py
# @Author: Nine-Tales
# @Date  : 2019-09-15
# @Desc  : 492.构造矩形

# 1. 你设计的矩形页面必须等于给定的目标面积.
# 2. 宽度 W 不应大于长度 L, 换言之, 要求 L >= W.
# 3. 长度 L 和宽度 W 之间的差距应当尽可能小.


def constructRectangle(area):
    l = int(area ** 0.5)
    while area%l !=0:
        l -= 1
    return [int(area/l), l]


# 构思: 主要采用了从平方根遍历的思路;
# 最开始尝试暴力破解, 效率低呀, 后来又有一些构思, 也不及这个快准狠.
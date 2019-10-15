#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/28 15:54 
# @Author : Nine-Tales
# @Desc: 172. 阶乘后的零

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def trailingZeroes(n):
    count = 0
    i = 5
    while i <= n:
        count += n // i
        i *= 5
    return count


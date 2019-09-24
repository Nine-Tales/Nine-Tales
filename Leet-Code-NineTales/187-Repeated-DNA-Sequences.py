#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/24 11:04 
# @Author : Nine-Tales
# @Desc: 187-重复DNA序列

from collections import defaultdict
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

def findRepeatedDnaSequences(s):
    visited = set()
    res = set()
    for i in range(0, len(s) - 9):
        tmp = s[i:i+10]
        if tmp in visited:
            res.add(tmp)
        visited.add(tmp)
    return list(res)

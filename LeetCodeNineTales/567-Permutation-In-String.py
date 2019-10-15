#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/24 9:38 
# @Author : Nine-Tales
# @Desc: 567-字符串的排列

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def checkInclusion(s1, s2):
    l1 = len(s1)
    l2 = len(s2)
    if l1 > l2:
        return False
    s = 'abcdefghijklmnopqrstuvwxyz'
    dict1 = {char: 0 for char in s}
    dict2 = {char: 0 for char in s}
    for i in range(l1):
        dict1[s1[i]] += 1
        dict2[s2[i]] += 1
    if dict1 == dict2:
        return True
    for j in range(l2 - l1):
        dict2[s2[j]] -= 1
        dict2[s2[j + l1]] += 1
        if dict1 == dict2:
            return True
    return False

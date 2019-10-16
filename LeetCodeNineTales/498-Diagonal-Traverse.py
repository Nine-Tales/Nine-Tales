#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/16 8:50 
# @Author : Nine-Tales
# @Desc: 498-对角线遍历
# 点评: 可能不需要什么数据结构思想, 整体思路比较容易理解

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class Solution(object):

    def findDiagonalOrder(self, matrix):
        m, n, r = len(matrix), len(matrix) and len(matrix[0]), []
        for l in range(m+n-1):
            temp = [matrix[i][l - i] for i in range(max(0, l+1-n), min(l+1, m))]
            r += temp if l % 2 else temp[::-1]
        return r

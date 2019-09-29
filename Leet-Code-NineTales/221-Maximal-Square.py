#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/29 16:56 
# @Author : Nine-Tales
# @Desc: 221. 最大正方形

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def maximalSquare(matrix):
    # if not matrix: return 0
    row = len(matrix)
    col = len(matrix[0])
    dp = [[0] * (col + 1) for _ in range(row + 1)]
    res = 0
    for i in range(1, row + 1):
        for j in range(1, col + 1):
            if matrix[i - 1][j - 1] == 1:
                dp[i][j] = min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]) + 1
                res = max(res, dp[i][j] ** 2)
    return res

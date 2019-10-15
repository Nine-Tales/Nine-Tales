#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/21 11:08 
# @Author : Nine-Tales
# @Desc: 1024-视频拼接

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

clips = [[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]]
T = 10


# 法1    DP算法动态规划
"""
def videoStitching(clips, T):
    dp = [T + 1] * (T + 1)
    dp[0] = 0
    for i in range(0, T+1):
        for c in clips:
            if c[0] <=i and c[1] >=i:
                dp[i] = min(dp[i], dp[c[0]]+1)
    return -1 if dp[T] == T + 1 else dp[T]
"""


# 法2 贪心算法;
def videoStitching(clips, T):
    t = 0
    res = 0
    while t < T:
        new_t = t
        for x in clips:
            if x[0] <= t and x[1] > new_t:
                new_t = x[1]
        if new_t > t:
            t = new_t
            res += 1
        else:
            break
    if t >= T:
        return res
    else:
        return -1


if __name__ == '__main__':
    ans = videoStitching(clips, T)
    print(ans)


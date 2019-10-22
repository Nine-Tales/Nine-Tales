#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/22 14:27 
# @Author : Nine-Tales
# @Desc: 1010. 总持续时间可被60整除的歌曲.

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from typing import List
from collections import defaultdict


def numPairsDivisibleBy60(time: List[int]) -> int:
    time = [t % 60 for t in time]
    d = defaultdict(int)
    res = 0
    for t in time:
        # 1. 先计数
        # 针对 [0, 0, 0] 特殊例, 要模60
        residue = (60 - t) % 60
        if residue in d:
            res += d[residue]
        d[t] += 1
    return res








#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/27 18:19 
# @Author : Nine-Tales
# @Desc: 164. 最大间距

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def maximumGap(nums):
    nums.sort()
    if len(nums) < 2:
        return 0
    else:
        cos_list = [nums[i+1] - nums[i] for i in range(len(nums)-1)]
        return max(cos_list)

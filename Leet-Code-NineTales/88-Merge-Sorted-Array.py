#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/6 16:41 
# @Author : Nine-Tales
# @Desc: 88. 合并两个有序数组

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def merge(nums1, m, nums2, n):
    nums1[m:m+n] = nums2
    nums1.sort()


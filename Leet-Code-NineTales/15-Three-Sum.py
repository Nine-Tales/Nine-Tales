#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/25 15:18 
# @Author : Nine-Tales
# @Desc: 15. 三数之和

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class Solution:

    def threeSum(self, nums):
        nums.sort()
        res, k = [], 0
        for k in range(len(nums) - 2):
            if nums[k] > 0:
                break   # 因为 j > i> k;
            if k > 0 and nums[k] == nums[k - 1]:
                continue    # 跳过相同的`nums[k]`;
            i, j = k + 1, len(nums) - 1
            while i < j:    # 双指针
                s = nums[k] + nums[i] + nums[j]
                if s < 0:
                    i += 1
                    while i < j and nums[i] == nums[i - 1]:
                        i += 1
                elif s > 0:
                    j -= 1
                    while i < j and nums[j] == nums[j + 1]:
                        j -= 1
                else:
                    res.append([nums[k], nums[i], nums[j]])
                    i += 1
                    j -= 1
                    while i < j and nums[i] == nums[i - 1]:
                        i += 1
                    while i < j and nums[j] == nums[j + 1]:
                        j -= 1
        return res



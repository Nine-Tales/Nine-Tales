#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/23 15:55 
# @Author : Nine-Tales
# @Desc: 二叉树

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/24 16:33 
# @Author : Nine-Tales
# @Desc: 501-二叉树搜索树中的众树

from typing import List

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class TreeNode(object):

    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    
    @staticmethod
    def find_mode(root: TreeNode) -> List[int]:
        hash_table = {}
        ans = []

        def dfs(roots: TreeNode):
            if not roots:
                return
            if roots.val in hash_table:
                hash_table[root.val] += 1
            else:
                hash_table[root.val] = 1
            if roots.left:
                dfs(roots.left)
            if roots.right:
                dfs(roots.right)
        if not root:
            return []
        dfs(root)
        max_count = max(list(hash_table.values()))
        for i in list(hash_table.keys()):
            if hash_table[i] == max_count:
                ans.append(i)
        return ans

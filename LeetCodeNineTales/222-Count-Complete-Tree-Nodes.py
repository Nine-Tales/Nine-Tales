#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/23 15:48 
# @Author : Nine-Tales
# @Desc: 222. 完全二叉树的节点个数

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


# 完全二叉树:
#   在完全二叉树中, 除了最底层节点可能没填满外, 其余每层节点数都达到最大值,
#   并且最下面一层的节点都集中在该层最左边的若干位置. 若最底层为第h层, 则该
#   层包含1 ~ 2^h个节点;


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:

    def countNodes(self, root: TreeNode):
        # ~~递归思路~~
        # if not root:
        #     return 0
        # return self.countNodes(root.left) + self.countNodes(root.right) + 1

        # ~~迭代思路~~
        """
                def leftTreeHigh(node):
            res = 0
            while node is not None:
                res += 1
                node = node.left
            return res

        res = 0

        while root is not None:
            l, r = leftTreeHigh(root.left), leftTreeHigh(root.right)
            if l == r:
                res += 2 ** l
                root = root.right
            else:
                res += 2 ** r
                root = root.left
        return res
        """

        def get_height(root):
            if not root:
                return 0
            return 1 + get_height(root.left)

        if not root:
            return 0

        h = get_height(root)

        if get_height(root.right) == h - 1:
            # 左子树是满二叉树
            return 2 ** (h - 1) + self.countNodes(root.right)
        else:
            return 2 ** (h - 2) + self.countNodes(root.left)






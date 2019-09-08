#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : DFS.py
# @Author: Nine-Tales
# @Date  : 2019-09-08
# @Desc  : 递归 + 遍历

# DFS: Depth First Search 深度优先搜索[回溯算法];
# BFS: Breadth First Search 广度优先搜索;

# 递归
"""
class Node(object):
    # 初始化一个节点, 需要为节点设置值
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class Node_1(object):
    def __init__(self, value):
        # 节点值
        self.value = value
        # 节点入度
        self.come = 0
        # 节点出度
        self.out = 0
        # 节点的邻居节点
        self.nexts = []
        # 在节点为from的情况下, 边的集合
        self.edges = []

class BinaryTree(object):
    # 创建二叉树, 完成
    # - 添加元素
    # - 广度遍历
    # - 深度遍历(先序, 中序, 后序)
    def __init__(self):
        self.root = None
        pass

    # 添加元素
    def addNode(self, val):
        # 创建队列结构存储节点
        nodeStack = [self.root, ]

        # 如果根节点为空
        if self.root == None:
            self.root = Node(val)
            print("添加根节点: {0}成功!!".format(self.root.val))
            return

        while len(nodeStack) > 0:
            # 队列元素出列
            p_node = nodeStack.pop()

            # 如果左子节点为空
            if p_node.left == None:
                p_node.left = Node(val)
                print("添加左子节点: {0}成功!!".format(p_node.left.val))
                return

            # 如果右子节点为空
            if p_node.right == None:
                p_node.right = Node(val)
                print("添加右子节点: {0}成功!!".format(p_node.right.val))
                return

            nodeStack.insert(0, p_node.left)
            nodeStack.insert(0, p_node.right)

    # 广度遍历(中序: 父节点 --> 左子节点 --> 右子节点)
    def bfs(self):
        nodeStack = [self.root, ]

        while len(nodeStack) > 0:
            my_node = nodeStack.pop()
            print(" --> ", my_node.val)

            if my_node.left is not None:
                nodeStack.insert(0, my_node.left)

            if my_node.right is not None:
                nodeStack.insert(0, my_node.right)

    # 深度优先(先序遍历)
    def preorder(self, start_node):
        if start_node == None:
            return

        print(start_node.val)
        self.preorder(start_node.left)
        self.preorder(start_node.right)

    # 深度优先(中序遍历)
    def inorder(self, start_node):
        if start_node == None:
            return

        self.inorder(start_node.left)
        print(start_node.val)
        self.inorder(start_node.right)

    # 深度优先(后序遍历)
    def outorder(self, start_node):
        if start_node == None:
            return
        self.outorder(start_node.left)
        self.outorder(start_node.right)
        print(start_node.val)


def main():
    bt = BinaryTree()
    bt.addNode(0)
    bt.addNode(1)
    bt.addNode(2)
    bt.addNode(3)
    bt.addNode(4)
    bt.addNode(5)
    bt.addNode(6)
    bt.addNode(7)
    bt.addNode(8)
    bt.addNode(9)

    print("广度遍历-->")
    bt.bfs()

    print("先序遍历-->")
    bt.preorder(bt.root)

    print("中序遍历-->")
    bt.inorder(bt.root)

    print("后序遍历-->")
    bt.outorder(bt.root)


if __name__ == '__main__':
    main()
"""

# 遍历
class Graph(object):
    def __init__(self, nodes, sides):
        # nodes表示用户输入的点，int型，sides表示用户输入的边，是一个二元组(u, v)
        # self.sequence是字典，key是点，value是与key相连的边
        self.sequence = {}
        # self.side是临时变量，主要用于保存与 指定点v 相连接的点
        self.side = []
        for node in nodes:
            for side in sides:
                u, v = side
                # 指定点与另一个点在同一个边(可能是源点u或者是终点v)中，则说明这个点与指定点是相连接的点,则需要将这个点放到self.side中
                if node == u:
                    self.side.append(v)
                elif node == v:
                    self.side.append(u)
            # 注意，这里属于第二层循环，第一层是nodes中的一个点，第二层主要是遍历属于这个点的所有边，然后将点和边组成字典
            # 这里的字典aequence的key是第一层循环里面的一个点，value是一个[],就是刚才的临时变量self.side
            self.sequence[node] = self.side
            self.side = []

    def dfs(self, node0):
        # queue本质堆栈，其实就是pop()了最后一个的列表，用来存放需要遍历的数据
        # order里面存放的是具体的访问路径
        queue, order = [], []
        # 先将初始节点，对于树就是根节点，放到queue中，从node0开始遍历
        queue.append(node0)
        # 直到queue空了，也就是说图或树的节点全都遍历完了。
        while queue:
            # queue不就是堆栈嘛，这里将堆栈里面的最后一个node拿出来，
            v = queue.pop()
            # 放到order中，就相当于已经遍历完了该node
            order.append(v)
            # 从sequence字典中，找到该key值为v的node，注意value其实就是一个[]，所以遍历该node相连的边表[]中的所有数据
            for w in self.sequence[v]:
                # 假如遍历这个[]中的数据不属于order，也不在queue中，说明这个点还没有访问过，于是加入queue,这里并不将其加入order中
                # 因为是深度优先，所以这个点node访问完了之后要去queue中拿最后一个元素，也就是node节点的孩子
                if w not in order and w not in queue:
                    # append操作是将node加入到queue的末尾，恰好每次弹出来的也是末尾，所以访问的是初始节点---儿子---孙子---曾孙子
                    queue.append(w)
        return order

    # bfs同理
    def bfs(self, node0):
        queue, order = [], []
        queue.append(node0)
        order.append(node0)
        while queue:
            v = queue.pop(0)
            for w in self.sequence[v]:
                if w not in order:
                    order.append(w)
                    queue.append(w)
        return order


def main():
    nodes = [i + 1 for i in range(8)]
    sides = [(1, 2),
             (1, 3),
             (2, 4),
             (2, 5),
             (4, 8),
             (5, 8),
             (3, 6),
             (3, 7),
             (6, 7)]
    G = Graph(nodes, sides)
    print(G.dfs(1))
    print(G.bfs(1))


if __name__ == '__main__':
    main()
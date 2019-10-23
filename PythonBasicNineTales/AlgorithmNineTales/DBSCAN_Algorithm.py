#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/23 11:24 
# @Author : Nine-Tales
# @Desc: DBSCAN聚类 numpy实现

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import numpy as np

def MyDBSCAN(D, eps, MinPts):
    """
    :param D: dataset`D` (a list of vectors)
    :param eps: threshold distance
    :param MinPts:  required number of points
    :return: a list of cluster labels; label -1 means noise
    """

    # 有两个保留值:
    #   -1 --- 噪音;
    #   0 --- 未标注数据;

    # 初始化所有标签为0.
    labels = [0] * len(D)

    # C 是 当前的cluster的ID.
    C = 0

    # 这个for循环目的是找到新的cluster节点. 一旦找到有效的种子节点,
    # 就会创建一个新的集群, 集群的增长由"expandCluster"程序处理.

    # 'P' 是 datapoint 的索引.
    for P in range(0, len(D)):

        # 只有那些没有被标记过的节点, 才能被选为种子节点, 即节点的label必须为0.
        if not (labels[P] == 0):
            continue

        # Find all of P's neighboring points.
        NeighborPts = regionQuery(D, P, eps)

        # If the number is below MinPts, this point is noise.
        # This is the only condition under which a point is labeled
        # NOISE--when it's not a valid seed point. A NOISE point may
        # later be picked up by another cluster as a boundary point
        # (this is the only condition under which a cluster label can change
        # -- from NOISE to something else).
        if len(NeighborPts) < MinPts:
            labels[P] = -1
        # Otherwise, if there are at least MinPts nearby, use this point as the
        # seed for a new cluster.
        else:
            C += 1
            growCluster(D, labels, P, NeighborPts, C, eps, MinPts)

    # ALL data has been clustered
    return labels


def growCluster(D, labels, P, NeighborPts, C, eps, MinPts):
    """
    用种子节点"P"增加一个新的cluster"C".
    这个函数搜索数据集, 查找属于这个新集群的所有点.
    当这个函数返回时,集群"C"就完成了.
    """
    # 将集群标签分配给种子节点.
    labels[P] = C

    # 观察"P"的每个邻居节点(邻居节点被称作Pn).
    # NeighborPts将会按照FIFO队列的节点来搜索---也就是说当我们发现
    # 集群的新的分支点时, 它将会增长. FIFO行为是通过while循环实现的
    # 并非for循环, 在NeighborPts中,节点将通过索引来表示.
    i = 0
    while i < len(NeighborPts):
        # 从队列中获取下一个节点.
        Pn = NeighborPts[i]

        # 处理NOISE节点, 将他变为cluster"C"的叶子节点.
        if labels[Pn] == -1:
            labels[Pn] = C

        # 否则, 如果Pn未被声明, 声明它成为C的一部分.
        elif labels[Pn] == 0:
            labels[Pn] = C

            # 找到Pn的所有邻节点.
            PnNeighborPts = regionQuery(D, Pn, eps)

            # 如果Pn至少有MinPts个邻节点的话, 他将变成分支节点.
            # 增加所有的邻节点到FIFO队列中以待搜索.
            if len(PnNeighborPts) >= MinPts:
                NeighborPts = NeighborPts + PnNeighborPts
            # 如果不足, 他将变成叶子节点.

        i += 1


def regionQuery(D, P, eps):
    # 在数据集"D"中找到距离"P"点"eps"范围内的所有点.
    neighbors = []

    for Pn in range(0, len(D)):
        # 如果距离低于阈值, 将其添加到neighbors中.
        if np.linalg.norm(D[P] - D[Pn]) < eps:
            neighbors.append(Pn)

    return neighbors







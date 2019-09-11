#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : DIJKSTRA.py
# @Author: Nine-Tales
# @Date  : 2019-09-11
# @Desc  : 迪杰特斯拉算法! 两种写法-[源自网络]


# graph是表示各顶点距离的矩阵, v0是起始点, P[V]的值为前驱点坐标,
# D[v]表示v0到v的最短路径长度和;
def shortPath_Dijkstra(graph, v0):
    n = len(graph)
    final, P, D = [0] * n, [0] * n, [0] * n
    k = 0
    # 初始化
    for i in range(n):
        D[i] = graph[v0][i]
    D[v0] = 0
    final[v0] = 1
    for v in range(1, n):
        min = float("Inf")
        for w in range(0, n):
            if not final[w] and D[w] < min:
                k = w
                min = D[w]
        final[k] = 1
        for w in range(0, n):
            if not final[w] and min + graph[k][w] < D[w]:
                D[w] = min + graph[k][w]
                P[w] = k
    return D


def dijkstra(graph, s):
    # 判断图是否为空，如果为空直接退出
    if graph is None:
        return None
    dist = [MAX_value] * len(graph)
    dist[s] = 0
    S = []
    Q = [i for i in range(len(graph))]
    dist_init = [i for i in graph[s]]
    while Q:
        u_dist = min([d for v, d in enumerate(dist_init) if v in Q])
        u = dist_init.index(u_dist)

        S.append(u)
        Q.remove(u)

        for v, d in enumerate(graph[u]):
            if 0 < d < MAX_value:
                if dist[v] > dist[u] + d:
                    dist[v] = dist[u] + d
                    dist_init[v] = dist[v]
    return dist

    pass


if __name__ == '__main__':
    MAX_value = 999999
    # graph_list = [[0, 9, MAX_value, MAX_value, MAX_value, 14, 15, MAX_value],
    #               [9, 0, 24, MAX_value, MAX_value, MAX_value, MAX_value, MAX_value],
    #               [MAX_value, 24, 0, 6, 2, 18, MAX_value, 19],
    #               [MAX_value, MAX_value, 6, 0, 11, MAX_value, MAX_value, 6],
    #               [MAX_value, MAX_value, 2, 11, 0, 30, 20, 16],
    #               [14, MAX_value, 18, MAX_value, 30, 0, 5, MAX_value],
    #               [15, MAX_value, MAX_value, MAX_value, 20, 5, 0, 44],
    #               [MAX_value, MAX_value, 19, 6, 16, MAX_value, 44, 0]]
    graph_list = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]

    distance = shortPath_Dijkstra(graph_list, 0)
    print(distance)
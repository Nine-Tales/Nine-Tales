#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 778-Swim-In-Rising-Water.py
# @Author: Nine-Tales
# @Date  : 2019-09-11
# @Desc  : 778-水位上升的泳池中游泳


import heapq  # 默认最小堆


def swimInWater(grid):
    n = len(grid)
    pq = []
    vis = set()
    dir = [0, -1, 0, 1, 0]
    # init
    heapq.heappush(pq, (grid[0][0], 0, 0))
    vis.add((0, 0))
    while len(pq) > 0:
        cost, x, y = heapq.heappop(pq)
        if x == n - 1 and y == n - 1:
            return cost
        for i in range(4):
            dx, dy = dir[i] + x, dir[i + 1] + y
            if 0 <= dx < n and 0 <= dy < n:
                if (dx, dy) in vis:
                    continue;
                vis.add((dx, dy))
                heapq.heappush(pq, (max(grid[dx][dy], cost), dx, dy))

    return -1


if __name__ == '__main__':
    grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]
    answer = swimInWater(grid)
    print(answer)





#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/15 16:15 
# @Author : Nine-Tales
# @Desc:

from __future__ import annotations

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from .utils import Stack
from abc import abstractmethod
from enum import IntEnum
from typing import List, NamedTuple, Generic, Optional, TypeVar, Set
import matplotlib.pyplot as plt
import numpy as np


class Cell(IntEnum):
    EMPTY = 255     # 正常节点
    BLOCKED = 0     # 障碍节点
    START = 100     # 迷宫入口
    END = 200       # 迷宫出口
    PATH = 150      # 搜寻路径


class MazeLocation(NamedTuple):
    row: int
    col: int


T = TypeVar("T")


class Maze:
    class _Node(Generic[T]):

        def __init__(self, state: T, parent: Optional[T],
                     cost: float = 0.0, heuristic: float = 0.0) -> None:
            self.state: T = state
            self.parent: Optional[T] = parent
            self.cost: float = cost
            self.heuristic: float = heuristic

        def __lt__(self, other: Maze._Node) -> bool:
            return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def __init__(self, rows: int = 10, cols: int = 10, sparse: float = 0.2,
                 seed: int = 365, start: MazeLocation = MazeLocation(0, 0),
                 end: MazeLocation = MazeLocation(9, 9), *,
                 grid: Optional[np.array] = None) -> None:
        np.random.seed(seed)
        self._start: MazeLocation = start
        self._end: MazeLocation = end

        if grid is None:
            self._grid: np.array = np.random.choice([Cell.BLOCKED, Cell.EMPTY],
                                                    (rows, cols), p=[sparse, 1 - sparse])
        else:
            self._grid: np.array = grid
        self._grid[start] = Cell.START
        self._grid[end] = Cell.END

    def _test_goal(self, m1: MazeLocation) -> bool:
        return m1 == self._end

    def _success(self, m1:MazeLocation) -> List[MazeLocation]:
        location: List[MazeLocation] = []
        row, col = self._grid.shape
        if m1.row + 1 < row and self._grid[m1.row + 1, m1.col] != Cell.BLOCKED:
            location.append(MazeLocation(m1.row + 1, m1.col))
        if m1.row - 1 >= 0 and self._grid[m1.row -1, m1.col] != Cell.BLOCKED:
            location.append(MazeLocation(m1.row - 1, m1.col))
        if m1.col + 1 < col and self._grid[m1.row, m1.col + 1] != Cell.BLOCKED:
            location.append(MazeLocation(m1.row, m1.col + 1))
        if m1.col - 1 >= 0 and self._grid[m1.row, m1.col - 1] != Cell.BLOCKED:
            location.append(MazeLocation(m1.row, m1.col - 1))
        return location

    def _draw(self, pause: float) -> None:
        plt.imshow(self._grid, cmap="rainbow", interpolation="nearest")
        plt.xticks([])
        plt.yticks([])
        plt.pause(interval=pause)
        plt.cla()

    def draw(self, colormap="rainbow") -> None:
        plt.close()
        fig, ax = plt.subplots()
        ax.imshow(self._grid, cmap=colormap)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.show()

    @abstractmethod
    def _search(self) -> Optional[Maze._Node]:
        """ 查找路径 """

    def show_path(self, pause: float = 0.5, *, plot: bool = True) -> None:
        if pause <= 0:
            raise ValueError("Pause 必须比0大!")
        path: Maze._Node = self._search()
        if path is None:
            print("没有找到路径")
            return
        path = path.parent
        while path.parent is not None:
            self._grid[path.state] = Cell.PATH
            if plot:
                self._draw(pause)
            path = path.parent

        print("Path Done")


class DepthFirstSearch(Maze):
    def _search(self) -> Optional[DepthFirstSearch._Node]:
        stack: Stack = Stack()
        initial: DepthFirstSearch._Node = self._Node(self._start, None)
        marked: Set[MazeLocation] = {initial.state}
        stack.push(initial)
        while stack:
            parent: DepthFirstSearch._Node = stack.pop()
            state: MazeLocation = parent.state
            if self._test_goal(state):
                return parent
            children: List[MazeLocation] = self._success(state)
            for child in children:
                if child not in marked:
                    marked.add(child)
                    stack.push(self._Node(child, parent))


def dfs(initial, _next, _test):
    s: Stack = Stack()
    marked = {initial}
    s.push(initial)
    while s:
        parent = s.pop()
        if _test(parent):
            return parent
        children = _next(parent)
        for child in children:
            if child not in marked:
                marked.add(child)
                s.push(child)


if __name__ == '__main__':
    maze = DepthFirstSearch(rows=100, cols=100, end=MazeLocation(99, 99), seed=91)
    maze.show_path(0.00000000001, plot=True)
    maze.draw()
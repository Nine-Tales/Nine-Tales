#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/15 16:07 
# @Author : Nine-Tales
# @Desc: 

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from abc import abstractmethod, ABC
from collections import deque

class Base(ABC):
    def __init__(self):
        self._container = deque()

    @abstractmethod
    def push(self, value):
        # push item
        pass

    @abstractmethod
    def pop(self):
        # pop item
        pass

    def __len__(self):
        return len(self._container)

    def __repr__(self):
        return f'{type(self).__name__}({list(self._container)})'


class Stack(Base):
    def push(self, value):
        self._container.append(value)

    def pop(self):
        return self._container.pop()
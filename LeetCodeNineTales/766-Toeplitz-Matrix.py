#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/26 15:02 
# @Author : Nine-Tales
# @Desc: 

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def isToeplitzMatrix(matrix):
    return not (True in [matrix[i][:-1] != matrix[i + 1][1:] for i in range(len(matrix) - 1)])
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/23 14:40 
# @Author : Nine-Tales
# @Desc: 

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from PythonBasicNineTales.AlgorithmNineTales.DBSCAN_Algorithm import MyDBSCAN
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                            random_state=0)

X = StandardScaler().fit_transform(X)

print("运行手写版DBSCAN")
my_labels = MyDBSCAN(X, eps=0.3, MinPts=10)

print("运行sklearn的DBSCAN")
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
skl_labels = db.labels_

for i in range(0, len(skl_labels)):
    if not skl_labels[i] == -1:
        skl_labels[i] += 1

num_disagree = 0

for i in range(0, len(skl_labels)):

    if not skl_labels[i] == my_labels[i]:
        print("Sklearn: ", skl_labels[i], "Mine: ", my_labels[i])
        num_disagree += 1

if num_disagree == 0:
    print("PASS --- All labels match!")
else:
    print("FAIL --- ", num_disagree, "labels don't match")
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/21 11:50 
# @Author : Nine-Tales
# @Desc: tf.nn.dynamic_rnn 和 MultiRNNCell 构建多层动态LSTM

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import tensorflow as tf
import numpy as np

X = tf.random_normal(shape=[3, 5, 6], dtype=tf.float32)
X = tf.reshape(X, [-1, 5, 6])
stacked_rnn = []

for i in range(3):
    stacked_rnn.append(tf.nn.rnn_cell.BasicLSTMCell(24))

lstm_multi = tf.nn.rnn_cell.MultiRNNCell(stacked_rnn)
output, state = tf.nn.dynamic_rnn(lstm_multi, X, time_major=False, dtype=tf.float32)

print(output.shape)

# 三个LSTM隐藏层
print(len(state))
# 第一个LSTM隐藏层
print(state[0].h.shape)  # LSTM中的h状态
print(state[0].c.shape)  # LSTM中的c状态
# 第二个LSTM隐藏层
print(state[1].h.shape)
print(state[1].c.shape)
# 第三个LSTM隐藏层
print(state[2].h.shape)
print(state[2].c.shape)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/20 9:17 
# @Author : Nine-Tales
# @Desc: 使用TF.ESTIMATOR 实现线性回归;

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import numpy as np
import tensorflow as tf


# 定义特性列, 线性模型中特性是列是x, shape=[1], 因此定义如下:
feature_columns = [tf.feature_column.numeric_column("x", shape=[1])]

# 使用tf.estimator内置的LinearRegressor来完成线性回归算法;
# tf.estimator提供了很多常规的算法模拟以便用户调用, 不需要用户自己重复造轮子;
# 到此为止, 短短两行代码, 我们的建模工作就已经完成了;
# estimator = tf.estimator.LinearRegressor(feature_columns=feature_columns)


def model_fn(features, labels, mode):
    # 用底层API构建线性模型
    W = tf.get_variable("W", [1], dtype=tf.float64)
    b = tf.get_variable("b", [1], dtype=tf.float64)
    y = W * features["x"] + b

    loss = tf.reduce_sum(tf.square(y - labels))

    # 获取训练全局参数step;
    global_step = tf.train.get_global_step()
    # 梯度下降算法. 学习率是0.01;
    optimizer = tf.train.GradientDescentOptimizer(0.01)
    # 将优化器和全局step的累加方法打包成一个方法组, 相当于把若干个方法打包成事务执行的模式;
    train = tf.group(optimizer.minimize(loss), tf.assign_add(global_step, 1))

    # 将所有内容封装成符合tf.estimator.Estimator规范的对象;
    return tf.estimator.EstimatorSpec(
        mode=mode,
        predictions=y,
        loss=loss,
        train_op=train
    )


# 自定义方法: 替换了estimator = tf.estimator.LinearRegressor(feature_columns=feature_columns)
estimator = tf.estimator.Estimator(model_fn=model_fn)

# 有了模型之后, 我们要使用模型完成训练->评估->预测这几个人步骤;
# 训练数据依旧是(1., 0.), (2., -1.), (3., -2.), (4., -3.)这几个人点, 拆成x和y两个维度的数组;
x_train = np.array([1., 2., 3., 4.])
y_train = np.array([0., -1., -2., -3.])

# 评估数据为(2., -1.01), (5., -4.1), (8., -7.), (1., 0.)这四个点, 同样拆分成x和y两个维度的数组
x_eval = np.array([2., 5., 8., 1.])
y_eval = np.array([-1.01, -4.1, -7., 0.])

# 用tf.estimator.numpy_input_fn方法生成随机打乱的数据组, 每组包含4个数据;
input_fn = tf.estimator.inputs.numpy_input_fn({"x": x_train}, y_train, batch_size=4,
                                              num_epochs=None, shuffle=True)
# 循环1000次训练模型;
estimator.train(input_fn=input_fn, steps=1000)

# 生成训练数据, 分成1000组, 每组4个数据;
train_input_fn = tf.estimator.inputs.numpy_input_fn({"x": x_train}, y_train,
                                                    batch_size=4, num_epochs=1000, shuffle=False)
# 生成评估数据, 分成1000组, 每组4个数据;
eval_input_fn = tf.estimator.inputs.numpy_input_fn({"x": x_eval}, y_eval, batch_size=4,
                                                   num_epochs=1000, shuffle=False)

# 训练数据在模型上的预测准确率
train_metrics = estimator.evaluate(input_fn=train_input_fn)
# 评估数据在模型上的预测准确率
eval_metrics = estimator.evaluate(input_fn=eval_input_fn)

print("训练指标: %r" % train_metrics)
print("评估指标: %r" % eval_metrics)
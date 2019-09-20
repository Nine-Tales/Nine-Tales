#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/20 10:52 
# @Author : Nine-Tales
# @Desc: 通过tf.estimator使用DNN-Classifier实现水仙花数据集

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import os
from six.moves.urllib.request import urlopen

import numpy as np
import tensorflow as tf

# 数据集
IRIS_TRAINING = "iris_training.csv"
IRIS_TRAINING_URL = "http://download.tensorflow.org/data/iris_training.csv"

IRIS_TEST = "iris_test.csv"
IRIS_TEST_URL = "http://download.tensorflow.org/data/iris_test.csv"

def main():
    # 先将数据集保存到本地
    if not os.path.exists(IRIS_TRAINING):
        raw = urlopen(IRIS_TRAINING_URL).read()
        with open(IRIS_TRAINING, "wb") as f:
            f.write(raw)

    if not os.path.exists(IRIS_TEST):
        raw = urlopen(IRIS_TEST_URL).read()
        with open(IRIS_TEST, "wb") as f:
            f.write(raw)

    # 读取数据集
    training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
        filename=IRIS_TRAINING,
        target_dtype=np.int,
        features_dtype=np.float32
    )
    test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
        filename=IRIS_TEST,
        target_dtype=np.int,
        features_dtype=np.float32
    )

    feature_columns = [tf.feature_column.numeric_column("x", shape=[4])]

    # 创建一个三层的DNN深度学习分类器, 三层分别有10, 20, 10个神经元;
    classifier = tf.estimator.DNNClassifier(
        feature_columns=feature_columns,
        hidden_units=[10, 20, 10],
        n_classes=3,
        model_dir="iris_model"
    )

    # 定义训练用的数据集输入;
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": np.array(training_set.data)},
        y=np.array(training_set.target),
        num_epochs=None,
        shuffle=True
    )

    # 训练模型;
    classifier.train(input_fn=train_input_fn, steps=2000)

    # 定义测试用的数据集输入
    test_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": np.array(test_set.data)},
        y=np.array(test_set.target),
        num_epochs=1,
        shuffle=False
    )

    # 评估准确率
    accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]

    print(" Test Accuracy: {0:f}".format(accuracy_score))

    # 预测两个新样本
    new_samples= np.array(
        [[6.4, 3.2, 4.5, 1.5],
         [5.8, 3.1, 5.0, 1.7]], dtype=np.float32
    )
    predict_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": new_samples},
        num_epochs=1,
        shuffle=False
    )

    predictions = list(classifier.predict(input_fn=predict_input_fn))

    predicted_classes = [p["classes"] for p in predictions]

    print(" New Samples, Class Predictions: {}".format(predicted_classes))


if __name__ == '__main__':
    main()
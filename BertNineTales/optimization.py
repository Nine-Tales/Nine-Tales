#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/16 15:39 
# @Author : Nine-Tales
# @Desc: 

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import tensorflow as tf


# 创建优化器
def create_optimizer(loss, init_lr, num_train_steps, num_warmup_steps, use_tpu):

    # tf.train.get_or_create_global_step(graph=None) -- return global step tensor
    global_step = tf.train.get_or_create_global_step()

    learning_rate = tf.constant(value=init_lr, shape=[], dtype=tf.float32)

    # 实现学习率的线性衰减;
    learning_rate = tf.train.polynomial_decay(
        learning_rate,
        global_step,
        num_train_steps,
        end_learning_rate=0.0,
        power=1.0,
        cycle=False
    )

    # 警告: if global_step < num_warmup_steps
    # 学习率 = global_step / num_warmup_steps * init_lr
    if num_warmup_steps:
        global_steps_int = tf.cast(global_step, tf.int32)
        warmup_steps_int = tf.constant(num_warmup_steps, dtype=tf.int32)

        global_steps_float = tf.cast(global_steps_int, tf.float32)
        warmup_steps_float = tf.cast(warmup_steps_int, tf.float32)

        warmup_percent_done = global_steps_float / warmup_steps_float
        warmup_learning_rate = init_lr * warmup_percent_done

        is_warmup = tf.cast(global_steps_int < warmup_steps_int, tf.float32)
        learning_rate = ((1.0 - is_warmup) * learning_rate + is_warmup * warmup_learning_rate)

    # 建议采用这个优化器;(请注意: Adam的m/v变量并没有从init_checkpoint中加载)
    optimizer = AdamWeightDecayOptimizer(
        learning_rate=learning_rate,
        weight_decay_rate=0.01,
        beta_1=0.9,
        beta_2=0.999,
        epsilon=1e-6,
        exclude_from_weight_decay=["LayerNorm", "layer_norm", "bias"]
    )

    # TPU路线
    if use_tpu:
        optimizer = tf.contrib.tpu.CrossShardOptimizer(optimizer)

    tvars = tf.trainable_variables()
    grads = tf.gradients(loss, tvars)

    # 模型如何预训练
    (grads, _) = tf.clip_by_global_norm(grads, clip_norm=1.0)

    train_op = optimizer.apply_gradients(
        zip(grads, tvars), global_step=global_step
    )

    # 通常 global step 更新会在"apply_gradients"中完成;
    # 但"AdamWeightDecayOptimizer"不会这么做; 如果你使用不同的优化器, 你应该注释这些内容;
    new_global_step = global_step + 1
    train_op = tf.group(train_op, [global_step.assign(new_global_step)])
    return train_op


# Adam优化器 bert定制版
class AdamWeightDecayOptimizer(tf.train.Optimizer):

    def __init__(self,
                 learning_rate,
                 weight_decay_rate=0.0,
                 beta_1=0.9,
                 beta_2=0.999,
                 epsilon=1e-6,
                 exclude_from_weight_decay=None,
                 name="AdamWeightDecayOptimizer"):
        # 构建一个AdamWeightDecayOptimizer
        super(AdamWeightDecayOptimizer, self).__init__(False, name)

        self.learning_rate = learning_rate
        self.weight_decay_rate = weight_decay_rate
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.epsilon = epsilon
        self.exclude_from_weight_decay = exclude_from_weight_decay

    def apply_gradients(self, grads_and_vars, global_step=None, name=None):
        # 对变量应用梯度求解, tf.train.Optimizer中的方法的overwrites
        assignments = []
        for (grad, param) in grads_and_vars:
            if grad is None or param is None:
                continue

            # 获取variable名称
            param_name = self._get_variable_name(param.name)

            m = tf.get_variable(
                name=param_name + "/adam_m",
                shape=param.shape.as_list(),
                dtype=tf.float32,
                trainable=False,
                initializer=tf.zeros_initializer()
            )

            v = tf.get_variable(
                name=param_name + "/adam_v",
                shape=param.shape.as_list(),
                dtype=tf.float32,
                trainable=False,
                initializer=tf.zeros_initializer()
            )

            # 更新基本的Adam方法;
            # m = b1 * m + (1 - b1) * g Momentum
            next_m = (tf.multiply(self.beta_1, m) + tf.multiply(1.0 - self.beta_1, grad))
            # v = b2 * v + (1 - b2) * g ** 2 AdaGrad
            next_v = (tf.multiply(self.beta_2, v) + tf.multiply(1.0 - self.beta_2, tf.square(grad)))

            update = next_m / (tf.sqrt(next_v) + self.epsilon)

            # L2正则
            if self._do_use_weight_decay(param_name):
                # w += 0.01 * l2
                update += self.weight_decay_rate * param

            update_with_lr = self.learning_rate * update

            # w = w - (lr * m / (v ** 1 / 2 + 1e - 6))
            next_param = param - update_with_lr

            assignments.extend(
                [param.assign(next_param),
                 m.assign(next_m),
                 v.assign(next_v)]
            )

        # 返回w, m, v
        return tf.group(*assignments, name=name)

    def _do_use_weight_decay(self, param_name):
        # 是否使用L2权重递减`param_name`
        if not self.weight_decay_rate:
            return False
        if self.exclude_from_weight_decay:
            for r in self.exclude_from_weight_decay:
                if re.search(r, param_name) is not None:
                    return False
        return True

    def _get_variable_name(self, param_name):
        # 从张量名称中获取变量名称
        m = re.match("^(.*):\\d+$", param_name)
        if m is not None:
            param_name = m.group(1)
        return param_name
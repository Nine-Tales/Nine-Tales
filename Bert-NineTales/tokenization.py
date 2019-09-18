#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/17 8:46 
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

import collections
import re
import unicodedata
import six
import tensorflow as tf


# 检验传入的参数是否符合规范
def validate_case_matches_checkpoint(do_lower_case, init_checkpoint):
    # 检验配置文件里的参数是否与checkpoint的名字相符;

    # 参数必须由用户传入, 所以没有显示检查[no explicit check]是否匹配checkpoint;
    # 参数信息大概率保存在bert_config.json文件中; 但是他没有; 所以我们必须启发式地检测它以进行验证;

    if not init_checkpoint:
        return

    m = re.match("^.*?([A-Za-z0-9_-]+)/bert_model.ckpt", init_checkpoint)
    if m is None:
        return

    model_name = m.group(1)

    lower_models = [
        "uncased_L-24_H-1024_A-16", "uncased_L-12_H-768_A-12",
        "multilingual_L-12_H-768_A-12", "chinese_L-12_H-768_A-12"
    ]

    cased_models = [
        "cased_L-12_H-768_A-12", "cased_L-24_H-1024_A-16",
        "multi_cased_L-12_H-768_A-12"
    ]

    is_bad_config = False

    if model_name in lower_models and not do_lower_case:
        is_bad_config = True
        actual_flag = "False"
        case_name = "lowercased"
        opposite_flag = "True"

    if model_name in cased_models and do_lower_case:
        is_bad_config = True
        actual_flag = "True"
        case_name = "cased"
        opposite_flag = "False"

    if is_bad_config:
        raise ValueError(
            "使用'--init_checkpoint=%s'传入'--do_lower_case=%s'."
            "然而, '%s' 好像是一个 %s 模型, 所以为了你的微调能匹配"
            "模型的预训练效果,你应该传入'--do_lower_case=%s', 如果"
            "这个error不正确, 请注释掉该行代码!" % (actual_flag, init_checkpoint,
                                       model_name, case_name, opposite_flag))


# 检验传入文本的编码格式
def convert_to_unicode(text):
    # 将`text`转为Unicode, 如果没有, 采用utf-8代替;
    if six.PY3:
        if isinstance(text, str):
            return text
        elif isinstance(text, bytes):
            return text.decode("utf-8", "ignore")
        else:
            raise ValueError("不支持的String类型: %s" % (type(text)))
    # 判断系统是否为python2的代码, 报错可注释掉
    # elif six.PY2:
    #     if isinstance(text, str):
    #         return text.decode("utf-8", "ignore")
    #     elif isinstance(text, unicode):
    #         return text
    #     else:
    #         raise ValueError("不支持的string类型: %s" % (type(text)))
    else:
        raise ValueError("请在Python2 或者 Python3 当中运行!!")


def printable_text(text):
    # 返回适合print的或`tf.logging`的编码的文本;

    # 调整Python2和Python3中`str`的`type`类型;
    # Python2是`Unicode`类型, Python3是`byte`类型;
    if six.PY3:
        if isinstance(text, str):
            return text
        elif isinstance(text, bytes):
            return text.decode("utf-8", "ignore")
        else:
            raise ValueError("不支持的String类型: %s" % (type(text)))
    # 判断系统是否为python2的代码, 报错可注释掉
    # elif six.PY2:
    #     if isinstance(text, str):
    #         return text
    #     elif isinstance(text, unicode):
    #         return text.encode("utf-8")
    #     else:
    #         raise ValueError("Unsupported string type: %s" % (type(text)))
    else:
        raise ValueError("请在Python2 或者 Python3 当中运行!!")


# 加载词汇表, 词汇表格式为 {"词": index}
def load_vocab(vocab_file):
    # 将词汇表文件加载到字典中;
    # 创建有序字典
    vocab = collections.OrderedDict()
    index = 0
    with tf.gfile.GFile(vocab_file, "r") as reader:
        while True:
            token = convert_to_unicode(reader.readline())
            if not token:
                break
            token = token.strip()
            vocab[token] = index
            index += 1
    return vocab


# 将{"词": index}变为[]
def convert_by_vocab(vocab, items):
    # 使用词汇转换[tokens | ids];
    output = []
    for item in items:
        output.append(vocab[item])
    return output


# 相互转换, 使用convert_by_vocab方法
def convert_tokens_to_ids(vocab, tokens):
    return convert_by_vocab(vocab, tokens)


def convert_ids_to_tokens(inv_vocab, ids):
    return convert_by_vocab(inv_vocab, ids)


# 文本清理, 去除文本中的空格等字符
def whitespace_tokenize(text):
    # 清除空格
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    return tokens


# 核心方法之一: 端到端的Tokenization;
class FullTokenizer(object):

    def __init__(self,
                 vocab_file,
                 do_lower_case=True):
        self.vocab = load_vocab(vocab_file)
        # {id: 内容}
        self.inv_vocab = {v: k for k, v in self.vocab.items()}

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
        self.basic_tokenizer = BasicTokenizer(do_lower_case=do_lower_case)
        self.wordpiece_tokenizer = WordpieceTokenizer(vocab=self.vocab)

    def tokenize(self, text):
        split_tokens = []
        for token in self.basic_tokenizer.tokenize(text):
            for sub_token in self.wordpiece_tokenizer.tokenize(token):
                split_tokens.append(sub_token)

        return split_tokens

    def convert_tokens_to_ids(self, tokens):
        return convert_by_vocab(self.vocab, tokens)

    def convert_ids_to_tokens(self, ids):
        return convert_by_vocab(self.inv_vocab, ids)


class BasicTokenizer(object):
    # 运行基本的分词(标点符号分割, 小写字母等);

    def __init__(self, do_lower_case=True):
        self.do_lower_case = do_lower_case

    def tokenize(self, text):
        # 标记一段文字
        text = convert_to_unicode(text)
        text = self._clean_text(text)

        # 添加了中文的版本
        text = self._tokenize_chinese_chars(text)

        orig_tokens = whitespace_tokenize(text)
        split_tokens = []
        for token in orig_tokens:
            if self.do_lower_case:
                token = token.lower()
                token = self._run_strip_accents(token)
            split_tokens.extend(self._run_split_on_punc(token))

        output_tokens = whitespace_tokenize(" ".join(split_tokens))
        return output_tokens

    def _run_strip_accents(self, text):
        # 从文本中删除重音符号
        text = unicodedata.normalize("NDF", text)
        output = []
        for char in text:
            cat = unicodedata.category(char)
            if cat == "Mn":
                continue
            output.append(char)
        return "".join(output)

    def _run_split_on_punc(self, text):
        # 拆分一段文字上的标点符号, 将文本转为list, 遍历去除符号后转为str
        chars = list(text)
        i = 0
        start_new_word = True
        output = []
        while i < len(chars):
            char = chars[i]
            if _is_punctuation(char):
                output.append([char])
                start_new_word = True
            else:
                if start_new_word:
                    output.append([])
                start_new_word = False
                output[-1].append(char)
            i += 1
        return ["".join(x) for x in output]

    def _tokenize_chinese_chars(self, text):
        # 在任何中文CJK字符中添加空格
        output = []
        for char in text:
            cp = ord(char)
            if self._is_chinese_char(cp):
                output.append(" ")
                output.append(char)
                output.append(" ")
            else:
                output.append(char)
        return "".join(output)

    def _is_chinese_char(self, cp):
        # 检查cp参数是否是CJK字符的codepoint
        if ((cp >= 0x4E00 and cp <= 0x9FFF) or
            (cp >= 0x3400 and cp <= 0x4DBF) or
            (cp >= 0x20000 and cp <= 0x2A6DF) or
            (cp >= 0x2A700 and cp <= 0x2B73F) or
            (cp >= 0x2B740 and cp <= 0x2B81F) or
            (cp >= 0x2B820 and cp <= 0x2CEAF) or
            (cp >= 0xF900 and cp <= 0xFAFF) or
                (cp >= 0x2F800 and cp <= 0x2FA1F)):
            return True

        return False

    def _clean_text(self, text):
        # 删除无效字符, 清理文本中的空白;
        output = []
        for char in text:
            cp = ord(char)
            if cp == 0 or cp == 0xfffd or _is_control(char):
                continue
            if _is_whitespace(char):
                output.append(" ")
            else:
                output.append(char)
        return "".join(output)


class WordpieceTokenizer(object):

    def __init__(self, vocab, unk_token="[UNK]", max_input_chars_per_word=200):
        self.vocab = vocab
        self.unk_token = unk_token
        self.max_input_chars_per_word = max_input_chars_per_word

    def tokenize(self, text):
        # 对一段文本进行分词工作, 使用给定的词汇;
        # 通过'最长匹配优先的贪心算法'执行标记;
        # 例如:
        #   input = "unaffable"
        #   output = ["un", "##aff", "##able"]
        #   :param text: 输入已经经过"BasicTokenizer"处理过的文本;
        #   :return: list 单词标记列表;
        text = convert_to_unicode(text)

        output_tokens = []
        for token in whitespace_tokenize(text):
            chars = list(token)
            if len(chars) > self.max_input_chars_per_word:
                output_tokens.append(self.unk_token)
                continue

            is_bad = False
            start = 0
            sub_tokens = []
            while start < len(chars):
                end = len(chars)
                cur_substr = None
                while start < end:
                    substr = "".join(chars[start:end])
                    if start > 0:
                        substr = "##" + substr
                    if substr in self.vocab:
                        cur_substr = substr
                        break
                    end -= 1
                if cur_substr is None:
                    is_bad = True
                    break
                sub_tokens.append(cur_substr)
                start = end

            if is_bad:
                output_tokens.append(self.unk_token)
            else:
                output_tokens.extend(sub_tokens)
        return output_tokens


def _is_whitespace(char):
    # 去除空格 \t \n \r 等
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True
    cat = unicodedata.category(char)
    if cat == "Zs":
        return True
    return False


def _is_control(char):
    # 查看"char"是不是一个control字符;
    if char == "\t" or char == "\n" or char == "\r":
        return False
    cat = unicodedata.category(char)
    if cat in ("Cc", "Cf"):
        return True
    return False


def _is_punctuation(char):
    # 是不是标点符号
    cp = ord(char)
    # 我们将所有非"字母"/"数字"/"ASCII"视为标点符号;
    if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
            (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
        return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
        return True
    return False
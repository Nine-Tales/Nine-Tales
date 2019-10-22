#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/22 16:01 
# @Author : Nine-Tales
# @Desc: 

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def read_from_file(directions):
    decode_set = ["utf-8", "gb18030", "ISO-8859-2", "gbk", "Error"]
    for k in decode_set:
        try:
            file = open(directions, "r", encoding= k)
            readfile = file.read()
            # 若是混合编码则将不可编码的字符替换为"?"
            # readfile = readfile.encode(encoding="utf-8", errors="replace")
            file.close()
            break
        except:
            if k == "Error":
                raise Exception("%s had noway to decode" % directions)
            continue
    return readfile



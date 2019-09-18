#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/18 15:58 
# @Author : Nine-Tales
# @Desc: dataframe转json的六种方式;

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import pandas as pd

df = pd.DataFrame([['a', 'b'], ['c', 'd']],
                  index=['row 1', 'row 2'],
                  columns=['col 1', 'col 2'])

df = df.to_json(orient='split')

df = df.to_json(orient='records')

# {"row 1":{"col 1":"a","col 2":"b"},"row 2":{"col 1":"c","col 2":"d"}}
df = df.to_json(orient='index')

# {"col 1":{"row 1":"a","row 2":"c"},"col 2":{"row 1":"b","row 2":"d"}}
df = df.to_json(orient='columns')

# [["a","b"],["c","d"]]
df = df.to_json(orient='values')

# {"schema": {"fields":[{"name":"index","type":"string"},
#                            {"name":"col 1","type":"string"},
#                            {"name":"col 2","type":"string"}],
#                 "primaryKey":["index"],
#                 "pandas_version":"0.20.0"},
#  "data": [{"index":"row 1","col 1":"a","col 2":"b"},
#             {"index":"row 2","col 1":"c","col 2":"d"}]}
df = df.to_json(orient='table')

print(df)
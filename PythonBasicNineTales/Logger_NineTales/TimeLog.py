#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/14 14:01 
# @Author : Nine-Tales
# @Desc: 

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from .handlers import MidnightRotatingFileHandler
import logging

def register_log():
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    if False:
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = MidnightRotatingFileHandler("logfile")

    logging.basicConfig(
        level=int("loglevel"),
        format=fmt,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[handler]
    )

    logging.getLogger(__name__).setLevel(int("logLevel"))
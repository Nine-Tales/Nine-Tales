#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/14 11:43 
# @Author : Nine-Tales
# @Desc: 

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import codecs
import datetime
from logging.handlers import BaseRotatingHandler


class MidnightRotatingFileHandler(BaseRotatingHandler):

    def __init__(self, filename):
        self.suffix = "%Y-%m-%d"
        self.date = datetime.date.today()
        super(BaseRotatingHandler, self).__init__(filename, mode="a", encoding="utf-8", delay=0)

    def shouldRollover(self, record):
        return self.date != datetime.date.today()

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.date = datetime.date.today()

    def _open(self):
        filename = "%s.%s" % (self.baseFilename, self.date.strftime(self.suffix))
        if self.encoding is None:
            stream = open(filename, self.mode)
        else:
            stream = codecs.open(filename, self.mode, self.encoding)
        if os.path.exists(self.baseFilename):
            try:
                os.remove(self.baseFilename)
            except OSError:
                pass
        try:
            os.symlink(filename, self.baseFilename)
        except OSError:
            pass
        return stream


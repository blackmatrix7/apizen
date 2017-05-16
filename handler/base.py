# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2017/1/5 10:23
# Author: Matrix
# Site:
# File: base.py
# Software: PyCharm
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    def set_default_headers(self):
        pass


class SysBaseHandler(BaseHandler):
    pass


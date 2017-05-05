# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2017/1/5 10:23
# Author: Vcan
# Site:
# File: base.py
# Software: PyCharm
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    def set_default_headers(self):
        self.clear_header('Server')


class SysBaseHandler(BaseHandler):
    pass


class ApiBaseHandler(SysBaseHandler):
    pass


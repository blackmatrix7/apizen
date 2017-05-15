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


class ApiBaseHandler(SysBaseHandler):

    def __init__(self, application, request, **kwargs):
        self._access_token = None
        self._method = None
        self._app_key = None
        self._sign = None
        self._timestamp = None
        self._v = None
        self._format = 'json'
        SysBaseHandler.__init__(self, application, request, **kwargs)


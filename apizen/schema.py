#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/5/19 上午8:55
# @Author: Matrix
# @Site: https://github.com/blackmatrix7/apizen
# @File: schema.py
# @Software: PyCharm

__author__ = 'blackmatrix'


class _Http:

    def __init__(self):
        self._headers = {}
        self.host = None
        self.host_name = None
        self.method = None
        self.path = None
        self.protocol = None
        self.query = None
        self.version = None
        self.body = None

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers):
        # TODO 隔离不同web框架的headers，转换成统一格式的dict
        self._headers = {key: value for key, value in headers.items()}

Http = _Http()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/19 上午9:33
# @Author  : Matrix
# @Site    : 
# @File    : method.py
# @Software: PyCharm

__author__ = 'blackmatrix'


class ApiMethod:

    def __init__(self, name, func, method=('get', 'post'), enable=True, auth=False):
        self.name = name
        self.func = func
        self.method = method
        self.enable = enable
        self.auth = auth

if __name__ == '__main__':
    pass

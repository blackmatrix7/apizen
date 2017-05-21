#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/5/19 上午8:55
# @Author: Matrix
# @Site: https://github.com/blackmatrix7/apizen
# @File: schema.py
# @Software: PyCharm

__author__ = 'blackmatrix'


class Object(dict):
    pass


class List:

    def __init__(self, obj=None):
        if isinstance(obj, Object):
            raise ValueError
        else:
            self._obj = None

    def compare(self, value):
        if self._obj.keys() not in value.keys():
            return False


if __name__ == '__main__':
    test = {'key': {'value': 'a', 'hello': 'python'}, 'test': 1}
    print(test.keys())
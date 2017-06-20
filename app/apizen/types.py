#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/5/19 上午8:55
# @Author: Matrix
# @Site: https://github.com/blackmatrix7/apizen
# @File: types.py
# @Software: PyCharm
from copy import copy
__author__ = 'blackmatrix'


class _Typed:
    expected_type = type(None)

    def __call__(self, value):
        return self.expected_type(value)


class _Integer(_Typed):
    expected_type = int

    def __call__(self, value):
        return int(value) if isinstance(value, str) else value

Integer = _Integer()


class _String(_Typed):
    expected_type = str

String = _String()

if __name__ == '__main__':
    test = {'key': {'value': 'a', 'hello': 'python'}, 'test': 1}
    print(test.keys())

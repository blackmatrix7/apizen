#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/5/19 上午8:55
# @Author: Matrix
# @Site: https://github.com/blackmatrix7/apizen
# @File: types.py
# @Software: PyCharm
import json
from app.apizen.exceptions import ApiSysExceptions
__author__ = 'blackmatrix'


class _Typed:
    expected_type = type(None)

    def __call__(self, key, value):
        try:
            return self.expected_type(value)
        except ValueError:
            raise ApiSysExceptions.error_args_type('{0}：{1} <{2}>'.format(ApiSysExceptions.error_args_type.message, key, self.expected_type))


class _Integer(_Typed):
    expected_type = int

    def __call__(self, key, value):
        return int(value) if isinstance(value, str) else value

Integer = _Integer()


class _String(_Typed):
    expected_type = str

String = _String()


class _Float(_Typed):
    expected_type = float

Float = _Typed()


class _DictAndList(_Typed):
    expected_type = dict

    def __call__(self, key, value):
        return json.loads(value) if isinstance(value, str) else value

Dict = _DictAndList()

List = _DictAndList()

if __name__ == '__main__':
    test = {'key': {'value': 'a', 'hello': 'python'}, 'test': 1}
    print(test.keys())

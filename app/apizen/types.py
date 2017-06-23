#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/5/19 上午8:55
# @Author: Matrix
# @Site: https://github.com/blackmatrix7/apizen
# @File: types.py
# @Software: PyCharm
import json
from app.database import db
__author__ = 'blackmatrix'


class Typed:
    expected_type = type(None)

    def __call__(self, value):
        return self.expected_type(value)


class TypeInteger(Typed):
    expected_type = int

    def __call__(self, value):
        return int(value) if isinstance(value, str) else value

Integer = TypeInteger()


class TypeString(Typed):
    expected_type = str

String = TypeString()


class TypeFloat(Typed):
    expected_type = float

Float = TypeFloat()


class TypeDict(Typed):
    expected_type = dict

    def __call__(self, value):
        return json.loads(value) if isinstance(value, str) else value


Dict = TypeDict()


class TypeList:

    def __call__(self, typed, value):
        if isinstance(typed, db.Model):
            return typed(**value)
        else:
            return typed(value)


List = TypeList()


if __name__ == '__main__':
    test = {'key': {'value': 'a', 'hello': 'python'}, 'test': 1}
    print(test.keys())

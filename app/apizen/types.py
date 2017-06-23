#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/5/19 上午8:55
# @Author: Matrix
# @Site: https://github.com/blackmatrix7/apizen
# @File: types.py
# @Software: PyCharm
import json
import copy
from app.database import db
from datetime import datetime
from functools import partial
__author__ = 'blackmatrix'


class Typed:

    def __call__(self, *args, **kwargs):
        pass


class TypeBase(Typed):
    expected_type = type(None)

    def _convert(self, value):
        _value = copy.copy(value)
        return self.expected_type(_value)

    def __call__(self, value):
        _value = self._convert(value)
        if isinstance(_value, self.expected_type):
            return _value
        else:
            raise ValueError


class TypeInteger(TypeBase):
    __name__ = 'Integer'
    expected_type = int

    def _convert(self, value):
        _value = copy.copy(value)
        return int(_value) if isinstance(_value, str) else _value


class TypeString(TypeBase):
    __name__ = 'String'
    expected_type = str


class TypeFloat(TypeBase):
    __name__ = 'Float'
    expected_type = float


class TypeDateTime(Typed):
    __name__ = 'DateTime'
    expected_type = datetime

    def _convert(self, format_, value):
        _value = copy.copy(value)
        return self.expected_type.strptime(_value, format_) if isinstance(_value, str) else _value

    def __call__(self, format_, value=None):
        if value is None:
            return partial(self.__call__, format_=format_)
        _value = self._convert(format_, value)
        if isinstance(_value, self.expected_type):
            return _value
        else:
            raise ValueError


class TypeDict(TypeBase):
    __name__ = 'Dict'
    expected_type = dict

    def __call__(self, value):
        return json.loads(value) if isinstance(value, str) else value


class TypeList:

    def __call__(self, typed, value):
        if isinstance(typed, db.Model):
            return typed(**value)
        else:
            return typed(value)


Integer = TypeInteger()
String = TypeString()
Float = TypeFloat()
Dict = TypeDict()
List = TypeList()


if __name__ == '__main__':
    test = {'key': {'value': 'a', 'hello': 'python'}, 'test': 1}
    print(test.keys())

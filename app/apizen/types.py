#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/5/19 上午8:55
# @Author: Matrix
# @Site: https://github.com/blackmatrix7/apizen
# @File: types.py
# @Software: PyCharm
import json
import copy
from datetime import datetime
from json import JSONDecodeError
from .exceptions import ApiSysExceptions
from abc import ABCMeta, abstractmethod

__author__ = 'blackmatrix'


class Typed(metaclass=ABCMeta):

    @abstractmethod
    def _convert(self, *args, **kwargs):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class TypeBase(Typed):
    expected_type = type(None)

    def _convert(self, value):
        _value = copy.copy(value)
        return self.expected_type(_value)

    def __call__(self, *, value):
        _value = self._convert(value)
        if isinstance(_value, self.expected_type):
            return _value
        else:
            raise ValueError


class Integer(TypeBase):
    expected_type = int

    def _convert(self, value):
        _value = copy.copy(value)
        return int(_value) if isinstance(_value, str) else _value


class String(TypeBase):
    expected_type = str


class Float(TypeBase):
    expected_type = float


class DateTime(Typed):
    expected_type = datetime

    def _convert(self, format_, value):
        _value = copy.copy(value)
        return self.expected_type.strptime(_value, format_) if isinstance(_value, str) else _value

    def __init__(self, format_='%Y-%m-%d %H:%M:%S'):
        self.format_ = format_

    def __call__(self, value=None):
        _value = self._convert(self.format_, value)
        if isinstance(_value, self.expected_type):
            return _value
        else:
            raise ValueError


def convert(key, value, default_value, type_hints):
    type_ = 'Unknown'
    try:
        if value != default_value:
            # 系统级别 type hints 兼容 （兼顾历史接口代码）
            _type_hints = {
                int: Integer,
                float: Float,
                str: String,
                datetime: DateTime
            }.get(type_hints, type_hints)
            if issubclass(_type_hints, Typed):
                _type_hints = _type_hints()
            if isinstance(_type_hints, Typed):
                type_ = _type_hints.__class__.__name__
                value = _type_hints(value=value)
    except JSONDecodeError:
        raise ApiSysExceptions.invalid_json
    except ValueError:
        api_ex = ApiSysExceptions.error_args_type
        api_ex.message = '{0}：{1} <{2}>'.format(api_ex.message, key, type_)
        raise api_ex
    else:
        return value

#
# class TypeList(Typed):
#     __name__ = 'List'
#     expected_type = list
#
#     def _convert(self, type_, value):
#         _value = copy.copy(value)
#         return self.expected_type(list)
#
#     def __call__(self, type_, value):
#         if value is None:
#             return partial(self.__call__, typed=type_)
#         if isinstance(value, db.Model):
#             return type_(**value)
#         else:
#             return type_(value)
#
#
# class TypeDict(TypeBase):
#     __name__ = 'Dict'
#     expected_type = dict
#
#     def __call__(self, value):
#         return json.loads(value) if isinstance(value, str) else value


if __name__ == '__main__':
    test = {'key': {'value': 'a', 'hello': 'python'}, 'test': 1}
    print(test.keys())

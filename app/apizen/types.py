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


class IType(metaclass=ABCMeta):
    """
    自动类型转换需要实现IType接口，提供__call__方法，接受一个KeyOnly的参数value
    并进行类型转换，返回转换后的值，无法转换时，抛出ValueError
    """
    @abstractmethod
    def __call__(self, *, value):
        pass


class TypeBase(IType):
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


class DateTime(IType):
    expected_type = datetime

    def _convert(self, format_, value):
        _value = copy.copy(value)
        return self.expected_type.strptime(_value, format_) if isinstance(_value, str) else _value

    def __init__(self, format_='%Y-%m-%d %H:%M:%S'):
        self.format_ = format_

    def __call__(self, *, value):
        _value = self._convert(self.format_, value)
        if isinstance(_value, self.expected_type):
            return _value
        else:
            raise ValueError


class Dict(IType):
    expected_type = dict

    @staticmethod
    def _convert(value):
        return json.loads(value) if isinstance(value, str) else value

    def __call__(self, *, value):
        _value = self._convert(value)
        if isinstance(_value, self.expected_type):
            return _value
        else:
            raise ValueError


class List(IType):
    expected_type = list

    def __init__(self, type_=None):
        self.typed_ = type_

    def __call__(self, *, value):
        _value = json.loads(value) if isinstance(value, str) else value
        if self.typed_ is not None:
            _value = list(map(lambda item: self.typed_(item), _value))
        if isinstance(_value, self.expected_type):
            return _value
        else:
            raise ValueError


def _convert(type_hints, value):
    instance = type_hints() if issubclass(type_hints, IType) else type_hints
    if isinstance(instance, IType):
        type_ = instance.__class__.__name__
        value = instance(value=value)
    else:
        type_ = 'Unknown'
    return type_, value


def convert(key, value, default_value, type_hints):
    type_ = 'Unknown'
    try:
        if value != default_value:
            # 系统级别 type hints 兼容 （兼顾历史接口代码）
            _type_hints = {
                int: Integer,
                float: Float,
                str: String,
                list: List,
                dict: Dict,
                datetime: DateTime
            }.get(type_hints, type_hints)
            type_, value = _convert(_type_hints, value)
    except JSONDecodeError:
        raise ApiSysExceptions.invalid_json
    except ValueError:
        api_ex = ApiSysExceptions.error_args_type
        api_ex.message = '{0}：{1} <{2}>'.format(api_ex.message, key, type_)
        raise api_ex
    else:
        return value


if __name__ == '__main__':
    test = {'key': {'value': 'a', 'hello': 'python'}, 'test': 1}
    print(test.keys())

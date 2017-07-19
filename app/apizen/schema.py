#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/5/19 上午8:55
# @Author: Matrix
# @Site: https://github.com/blackmatrix7/apizen
# @File: types.py
# @Software: PyCharm
import re
import json
import copy
from json import JSONDecodeError
from datetime import datetime, date
from .exceptions import ApiSysExceptions

__author__ = 'blackmatrix'

"""
继承自某个内建类型，是为了解决Pycharm关于type hints的警告。
比如在一个函数中，type hints 使用自定义的DateTime，然后在函数内部使用了obj.year的方法，
因为DateTime本身与内建的datetime类型没有继承关系，并且没有year属性，Pycharm就会提示DateTime类型没有year属性的警告。
而type hints在接口参数中大量使用，这样会导致过多的警告信息。
为了解决这个问题，只好在类继承中，继承自某个内建的类型，然后通过元类，在创建类时，忽略掉内建类型的继承关系。
什么时候Pycharm不显示这个弱智的警告，就可以把内建类型的继承关系给取消了。

实质上,元类和继承系统内建的类型都是不必要的。不介意警告信息的话可以去除,让代码更加容易阅读。
"""


class Typed:

    @staticmethod
    def convert(*, value):
        return value


class TypeMeta(type):

    def __init__(cls,  classname, supers, clsdict):
        type.__init__(cls,  classname, supers, clsdict)

    def __new__(mcs, classname, supers, clsdict):
        return type.__new__(mcs, classname, (Typed, object), clsdict)


class TypeBase(metaclass=TypeMeta):
    pass


class _Integer(int, TypeBase):
    __type__ = 'Integer'

    @staticmethod
    def convert(*, value):
        _value = copy.copy(value)
        _value = int(_value) if isinstance(_value, str) else _value
        if isinstance(_value, int):
            return _value
        else:
            raise ValueError


class _String(str, TypeBase):
    __type__ = 'String'

    @staticmethod
    def convert(*, value):
        return str(value)


class _Float(float, TypeBase):
    __type__ = 'Float'

    @staticmethod
    def convert(*, value):
        _value = copy.copy(value)
        return float(_value)


class _Dict(dict, TypeBase):
    __type__ = 'Dict'

    @staticmethod
    def convert(*, value):
        _value = copy.copy(value)
        _value = json.loads(_value) if isinstance(_value, str) else _value
        if isinstance(_value, dict):
            return _value
        else:
            raise ValueError


class _List(list, TypeBase):
    __type__ = 'List'

    @staticmethod
    def convert(*, value):
        _value = copy.copy(value)
        _value = json.loads(_value) if isinstance(_value, str) else _value
        if isinstance(_value, list):
            return _value
        else:
            raise ValueError


class _Date(date, TypeBase):
    __type__ = 'DateTime'

    def convert(self, *, value=None):
        _value = copy.copy(value)
        _value = datetime.strptime(_value, self.format_) if isinstance(_value, str) else _value
        return _value

    def __init__(self, format_='%Y-%m-%d'):
        self.format_ = format_
        super().__init__()


class _DateTime(datetime, TypeBase):
    __type__ = 'DateTime'

    def convert(self, *, value=None):
        _value = copy.copy(value)
        _value = datetime.strptime(_value, self.format_) if isinstance(_value, str) else _value
        return _value

    def __init__(self, format_='%Y-%m-%d %H:%M:%S'):
        self.format_ = format_
        super().__init__()


class _Bool(bool, TypeBase):

    __type__ = 'Bool'

    @staticmethod
    def convert(*, value=None):
        _value = str(value).lower()
        if _value in ('true', 'yes', '是', '0'):
            _value = True
        elif _value in ('false', 'no', '否', '1'):
            _value = False
        else:
            _value = value
        if isinstance(_value, bool):
            return _value
        else:
            raise ValueError


class _Email(_String):
    __type__ = 'Email'

    @staticmethod
    def convert(*, value):
        if re.match('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', value, flags=0):
            return value
        else:
            raise ValueError


class _Model(TypeBase):

    def __init__(self, model):
        self.model = model

    def convert(self, *, value=None):
        data = json.loads(value) if isinstance(value, str) else value
        result = self.model(**{key: value for key, value in data.items() if key in self.model.__table__.columns})
        result.raw_data = data
        return result


class _Money(_Float):

    __type__ = 'Money'

    @staticmethod
    def convert(*, value):
        value = float(value)
        if value >= 0 and value == round(value, 2):
            return value
        else:
            raise ValueError


Integer = _Integer()
List = _List()
Money = _Money()
Bool = _Bool()
Float = _Float()
String = _String()
Dict = _Dict()
Date = _Date
Model = _Model
DateTime = _DateTime
Email = _Email


def dict2model(data, model):
    """
    实验性功能，将dict转换成sqlalchemy model，不能处理 relationship
    :param data:
    :param model:
    :return:
    """
    data = json.loads(data) if isinstance(data, str) else data
    result = model(**{key: value for key, value in data.items() if key in model.__table__.columns})
    result.raw_data = data
    return result


def convert(key, value, default_value, type_hints):
    # 系统级别 type hints 兼容 （兼顾历史接口代码）
    _type_hints = {
        int: Integer,
        float: Float,
        str: String,
        list: List,
        dict: Dict,
        datetime: DateTime
    }.get(type_hints, type_hints)
    try:
        if value != default_value:
            instance = _type_hints if isinstance(_type_hints, Typed) else _type_hints() if issubclass(_type_hints, Typed) else object()
            if isinstance(instance, Typed):
                value = instance.convert(value=value)
            return value
    except JSONDecodeError:
        raise ApiSysExceptions.invalid_json
    except ValueError:
        api_ex = ApiSysExceptions.error_args_type
        api_ex.err_msg = '{0}：{1} <{2}>'.format(api_ex.err_msg, key, _type_hints.__type__)
        raise api_ex
    else:
        return value

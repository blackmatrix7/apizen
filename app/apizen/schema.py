#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/5/19 上午8:55
# @Author: Matrix
# @Site: https://github.com/blackmatrix7/apizen
# @File: types.py
# @Software: PyCharm
import json
import copy
import types
from app.database import db
from json import JSONDecodeError
from datetime import date, datetime
from .exceptions import ApiSysExceptions
from abc import ABCMeta, abstractmethod
__author__ = 'blackmatrix'


class ITypeBase(metaclass=ABCMeta):

    def __new__(cls, cls_name, *args, **kwargs):
        return type.__new__(cls, cls_name, (object, ), {})

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def convert(*, value):
        pass


class Integer(int, ITypeBase):

    @staticmethod
    def convert(*, value):
        _value = copy.copy(value)
        if isinstance(_value, str):
            if _value.strip() == '':
                return None
            else:
                return int(_value)
        else:
            return _value


class String(str, ITypeBase):
    __name__ = 'String'

    @staticmethod
    def convert(*, value):
        _value = copy.copy(value)
        return str(_value)


class Float(float, ITypeBase):
    __name__ = 'Float'

    @staticmethod
    def convert(*, value):
        _value = copy.copy(value)
        return float(_value)


class Dict(dict, ITypeBase):
    __name__ = 'Dict'

    @staticmethod
    def convert(*, value):
        return json.loads(value) if isinstance(value, str) else value


class List(list, ITypeBase):
    __name__ = 'List'

    @staticmethod
    def convert(*, value):
        return json.loads(value) if isinstance(value, str) else value


# class DateTime(ITypeBase, date):
#     __name__ = 'DateTime'
#
#     def convert(self, *, value=None):
#         _value = copy.copy(value)
#         return datetime.strptime(_value, self.format_) if isinstance(_value, str) else _value
#
#     # def __new__(cls, format_='%Y-%m-%d %H:%M:%S'):
#     #     new_cls = types.new_class('DateTime', bases=(ITypeBase, object))
#     #     return new_cls
#
#     def __init__(self, format_='%Y-%m-%d %H:%M:%S'):
#         self.format_ = format_
#         super().__init__(format_=format_)


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


def _convert(type_hints, value):
    instance = type_hints() if issubclass(type_hints, ITypeBase) else type_hints
    if isinstance(instance, ITypeBase):
        value = instance.convert(value=value)
    elif issubclass(type_hints, db.Model):
        value = dict2model(value, type_hints)
    return value


def convert(key, value, default_value, type_hints):
    try:
        if value != default_value:
            # 系统级别 type hints 兼容 （兼顾历史接口代码）
            _type_hints = {
                int: Integer,
                float: Float,
                str: String,
                list: List,
                dict: Dict
            }.get(type_hints, type_hints)
            value = _convert(_type_hints, value)
    except JSONDecodeError:
        raise ApiSysExceptions.invalid_json
    except ValueError:
        api_ex = ApiSysExceptions.error_args_type
        api_ex.message = '{0}：{1} <{2}>'.format(api_ex.message, key, type_hints.__name__)
        raise api_ex
    else:
        return value


if __name__ == '__main__':
    test = {'key': {'value': 'a', 'hello': 'python'}, 'test': 1}
    print(test.keys())

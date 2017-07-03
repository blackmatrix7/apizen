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

"""
一定要继承自某个内建类型，是为了避免Pycharm的警告信息
强迫症看着烦，继承内建类型这层关系，在元类部分被暂时忽略
掉了。
什么时候Pycharm不显示这个弱智的警告，就可以把元类和内建类型
的继承关系给取消了。
"""


class TypeBase:

    # def __new__(cls, *args, **kwargs):
    #     return object.__new__(ITypeBase, *args)

    @staticmethod
    def convert(*, value):
        return value


class TypeMeta(type):

    def __new__(mcs, classname, supers, clsdict):
        return type.__new__(mcs, classname, (TypeBase, object), clsdict)


class Integer(int, metaclass=TypeMeta):

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


class String(str, metaclass=TypeMeta):
    __name__ = 'String'

    @staticmethod
    def convert(*, value):
        _value = copy.copy(value)
        return str(_value)


class Float(float, metaclass=TypeMeta):
    __name__ = 'Float'

    @staticmethod
    def convert(*, value):
        _value = copy.copy(value)
        return float(_value)


class Dict(dict, metaclass=TypeMeta):
    __name__ = 'Dict'

    @staticmethod
    def convert(*, value):
        return json.loads(value) if isinstance(value, str) else value


class List(list, metaclass=TypeMeta):
    __name__ = 'List'

    @staticmethod
    def convert(*, value):
        return json.loads(value) if isinstance(value, str) else value


class DateTime(date, metaclass=TypeMeta):
    __name__ = 'DateTime'

    def convert(self, *, value=None):
        _value = copy.copy(value)
        return datetime.strptime(_value, self.format_) if isinstance(_value, str) else _value

    # 因为在元类中，对超类的继承关系做了变动，这样导致的后果是很难通过编写__new__方法正确的创建类实例
    # 所以暂时无法解决 __new__ 和 __init__ 函数签名不一致的警告
    # TODO 解决 __new__ 和 __init__ 函数签名不一致的警告
    def __init__(self, format_='%Y-%m-%d %H:%M:%S'):
        self.format_ = format_


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
            instance = type_hints if isinstance(_type_hints, TypeBase) else type_hints() if issubclass(_type_hints, TypeBase) else object()
            if isinstance(instance, TypeBase):
                value = instance.convert(value=value)
            elif issubclass(type_hints, db.Model):
                value = dict2model(value, type_hints)
            return value
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

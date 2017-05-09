# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/3/14 8:43
# @Author: Matrix
# @Site:
# @File: api_list.py
# @Software: PyCharm
from services.demo.api_demo import ApiDemo

__author__ = 'matrix'

api_demo = ApiDemo()

api_version = {}


# Web Api版本注册
def version(v, enable=True):
    def _version(aclass):
        if enable:
            api_version[v] = aclass
        return aclass
    return _version


class ApiMethodMeta(type):

    def __new__(mcs, classname, supers, classdict):
        # 遍历父类的方法,获取父类版本的API方法
        all_api_methods = {}
        for super_ in supers:
            if super_ and 'api_methods' in super_.__dict__:
                super_methods = getattr(super_, 'api_methods')
                all_api_methods.update(super_methods)
        aclass = type.__new__(mcs, classname, supers, classdict)
        all_api_methods.update(getattr(aclass, 'support_methods'))
        setattr(aclass, 'api_methods', all_api_methods)
        return aclass


class ApiMethodBase(metaclass=ApiMethodMeta):

    api_methods = {}

    support_methods = {
        'matrix.api.demo.func1': {'func': api_demo.demo1},
        'matrix.api.demo.func2': {'func': api_demo.demo2}
    }


@version('1.0')
class ApiMethodV10(ApiMethodBase):
    support_methods = {
        'matrix.api.demo.func3': {'func': api_demo.demo3},
        'matrix.api.demo.func4': {'func': api_demo.demo4},
        'matrix.api.demo.func5': {'func': api_demo.demo5}
    }


@version('1.1')
class ApiMethodV11(ApiMethodV10):
    support_methods = {
        'matrix.api.demo.demo3': {'func': None},
        'matrix.api.demo.demo4': {'func': None}
    }


@version('1.2', enable=False)
class ApiMethodV12(ApiMethodV11):
    support_methods = {
        'matrix.api.demo.demo3': {'func': api_demo.demo3}
    }


if __name__ == '__main__':
    api_list = ApiMethodV12.api_methods
    print(api_version)
    print(api_list)

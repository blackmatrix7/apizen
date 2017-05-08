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

api = {
    '1.0':
        {
            'matrix.api.demo.demo1': {'func': api_demo.demo1},
            'matrix.api.demo.demo2': {'func': api_demo.demo2},
            'matrix.api.demo.demo3': {'func': api_demo.demo3},
            'matrix.api.demo.demo4': {'func': api_demo.demo4},
            'matrix.api.demo.demo5': {'func': api_demo.demo5}
        }
}


class ApiMethodMeta(type):

    def __new__(mcs, classname, supers, classdict):
        # 遍历父类的方法,获取父类版本的API方法
        all_support_methods = {}
        for super_ in supers:
            if 'support_methods' in super_.__dict__:
                super_methods = getattr(super_, 'support_methods')
                all_support_methods.update(super_methods)
        subclass = type.__new__(mcs, classname, supers, classdict)
        all_support_methods.update(getattr(subclass, '_support_methods'))
        setattr(subclass, 'support_methods', all_support_methods)
        return subclass


class ApiMethodBase(metaclass=ApiMethodMeta):

    support_methods = {}

    _support_methods = {
        'matrix.api.demo.demo1': {'func': api_demo.demo1},
        'matrix.api.demo.demo2': {'func': api_demo.demo2}
    }


class ApiMethodV10(ApiMethodBase):

    _support_methods = {
        'matrix.api.demo.demo1': {'func': api_demo.demo3},
        'matrix.api.demo.demo2': {'func': api_demo.demo4},
        'matrix.api.demo.demo3': {'func': api_demo.demo4}
    }


class ApiMethodV11(ApiMethodV10):

    _support_methods = {
        'matrix.api.demo.demo3': {'func': None},
        'matrix.api.demo.demo4': {'func': None}
    }


class ApiMethodV12(ApiMethodV11):

    _support_methods = {
        'matrix.api.demo.demo3': {'func': api_demo.demo3}
    }


if __name__ == '__main__':
    api_list = ApiMethodV12.support_methods
    print(api_list)

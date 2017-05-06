#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/5 下午3:29
# @Author  : Matrix
# @Site    : 
# @File    : api_demo.py
# @Software: PyCharm
from webapi.api_error import ApiSubError

__author__ = 'blackmatrix'


class ApiDemo:

    @staticmethod
    def demo1(user_id, age, name='刘峰'):
        return {
            'user_id': user_id,
            'name': name,
            'age': age
        }

    @staticmethod
    def demo2(**kwargs):
        return kwargs

    @staticmethod
    def demo3(user_id, **kwargs):
        return {
            'user_id': user_id,
            'other': kwargs
        }

    @staticmethod
    def demo4(*args):
        return args

    @staticmethod
    def demo5():
        print('r1sd')
        raise ApiSubError.unknown_error

    # 不支持VAR_POSITIONAL和KEYWORD_ONLY并存的函数参数
    @staticmethod
    def demo5(*args, user_id):
        return args, user_id

    # 不支持VAR_POSITIONAL和KEYWORD_ONLY并存的函数参数
    @staticmethod
    def demo5(*args, **kwargs):
        return args, kwargs

if __name__ == '__main__':
    pass

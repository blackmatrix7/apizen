#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/5 下午3:29
# @Author  : Matrix
# @Site    : 
# @File    : api_demo.py
# @Software: PyCharm
from functools import wraps
from webapi.api_error import ApiSubError

__author__ = 'blackmatrix'


def test_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(args, kwargs)
    return wrapper


class ApiDemo:

    @staticmethod
    @test_decorator
    def get_user(user_id, age, name='刘峰'):
        return {
            'user_id': user_id,
            'name': name,
            'age': age
        }

    @staticmethod
    def err_func(self):
        return self

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
    def raise_error():
        """
        抛出异常
        :return: 
        """
        raise ApiSubError.unknown_error
if __name__ == '__main__':
    pass

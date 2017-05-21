# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/3/14 8:43
# @Author: Matrix
# @Site:
# @File: api_list.py
# @Software: PyCharm
from apizen.version import ApiMethodBase, version
from services.demo.api_demo import ApiDemo

__author__ = 'matrix'

api_demo = ApiDemo()


@version(1.0)
class ApiMethodV10(ApiMethodBase):
    api_methods = {
        'matrix.api.set-user': {'func': api_demo.set_user},
        'matrix.api.set-users': {'func': api_demo.set_users},
        'matrix.api.return-err': {'func': api_demo.raise_error},
        'matrix.api.err-func': {'func': api_demo.err_func},
        'matrix.api.instance-func': {'func': api_demo.instance_func},
        'matrix.api.class-func': {'func': ApiDemo.class_method},
    }


@version(1.1)
class ApiMethodV11(ApiMethodV10):
    api_methods = {
        'matrix.api.send-kwargs': {'func': api_demo.send_kwargs},
        'matrix.api.raise-error': {'func': api_demo.raise_error},
        'matrix.api.speed-test': {'func': api_demo.speed_test},
    }


@version(1.2)
class ApiMethodV12(ApiMethodV11):
    api_methods = {
        'matrix.api.only-post': {'func': api_demo.raise_error, 'method': ['post']},
        'matrix.api.api-stop': {'func': api_demo.raise_error, 'enable': False}
    }


if __name__ == '__main__':
    api_list = ApiMethodV10.api_methods
    print(api_list)

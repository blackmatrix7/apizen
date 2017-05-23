# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/3/14 8:43
# @Author: Matrix
# @Site:
# @File: methods.py
# @Software: PyCharm
from apizen.version import ApiMethodsBase, version
from services.demo.apidemo import ApiDemo

__author__ = 'matrix'

apidemo = ApiDemo()


@version(1.0)
class ApiMethodsV10(ApiMethodsBase):
    api_methods = {
        'matrix.api.set-user': {'func': apidemo.set_user},
        'matrix.api.set-users': {'func': apidemo.set_users},
        'matrix.api.return-err': {'func': apidemo.raise_error},
        'matrix.api.err-func': {'func': apidemo.err_func},
        'matrix.api.instance-func': {'func': apidemo.instance_func},
        'matrix.api.class-func': {'func': ApiDemo.class_method},
    }


@version(1.1)
class ApiMethodsV11(ApiMethodsV10):
    api_methods = {
        'matrix.api.send-kwargs': {'func': apidemo.send_kwargs},
        'matrix.api.raise-error': {'func': apidemo.raise_error},
        'matrix.api.speed-test': {'func': apidemo.speed_test},
    }


@version(1.2)
class ApiMethodsV12(ApiMethodsV11):
    api_methods = {
        'matrix.api.only-post': {'func': apidemo.raise_error, 'method': ['post']},
        'matrix.api.api-stop': {'func': apidemo.raise_error, 'enable': False}
    }


if __name__ == '__main__':
    api_list = ApiMethodsV10.api_methods
    print(api_list)

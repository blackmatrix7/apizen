# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/3/14 8:43
# @Author: BlackMatrix
# @Site:
# @File: methods.py
# @Software: PyCharm
from app.apizen.version import ApiMethodsBase, version
from app.webapi.services.demo import demo

__author__ = 'blackmatrix'


@version(1.0)
class ApiMethodsV10(ApiMethodsBase):
    api_methods = {
        'matrix.api.set-user': {'func': demo.set_user},
        'matrix.api.set-users': {'func': demo.set_users},
        'matrix.api.return-err': {'func': demo.raise_error},
        'matrix.api.err-func': {'func': demo.err_func},
        'matrix.api.instance-func': {'func': demo.instance_func},
        'matrix.api.class-func': {'func': demo.class_method},
    }


@version(1.1)
class ApiMethodsV11(ApiMethodsV10):
    api_methods = {
        'matrix.api.send-kwargs': {'func': demo.send_kwargs},
        'matrix.api.raise-error': {'func': demo.raise_error},
        'matrix.api.speed-test': {'func': demo.speed_test},
    }


@version(1.2)
class ApiMethodsV12(ApiMethodsV11):
    api_methods = {
        'matrix.api.only-post': {'func': demo.raise_error, 'method': ['post']},
        'matrix.api.api-stop': {'func': demo.raise_error, 'enable': False}
    }


if __name__ == '__main__':
    api_list = ApiMethodsV10.api_methods
    print(api_list)

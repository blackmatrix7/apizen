# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/3/14 8:43
# @Author: Matrix
# @Site:
# @File: api_list.py
# @Software: PyCharm

from apizen.version import ApiMethodBase
from services.demo.api_demo import ApiDemo

__author__ = 'matrix'

api_demo = ApiDemo()

# allversion = {}
#
#
# def version(v, enable=True):
#     """
#     Web Api版本注册
#     :param v:  版本号
#     :param enable:  版本是否停用
#     :return:  无
#     """
#     def _version(cls):
#         if enable:
#             allversion[v] = cls
#         return cls
#     return _version


# @version('1.0')
class ApiMethodV10(ApiMethodBase):
    api_methods = {
        'matrix.api.set-user': {'func': api_demo.set_user},
        'matrix.api.set-users': {'func': api_demo.set_users},
        'matrix.api.return-err': {'func': api_demo.raise_error},
        'matrix.api.err-func': {'func': api_demo.err_func},
        'matrix.api.instance-func': {'func': api_demo.instance_func},
        'matrix.api.class-func': {'func': ApiDemo.class_method},
    }


class ApiMethodV11(ApiMethodV10):
    api_methods = {
        'matrix.api.send-kwargs': {'func': api_demo.send_kwargs},
        'matrix.api.raise-error': {'func': api_demo.raise_error},
        'matrix.api.speed-test': {'func': api_demo.speed_test},
        'matrix.api.only-post': {'func': api_demo.raise_error, 'method': ['post']},
        'matrix.api.api-stop': {'func': api_demo.raise_error, 'enable': False}
    }


if __name__ == '__main__':
    api_list = ApiMethodV10.api_methods
    print(api_list)

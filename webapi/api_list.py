# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/3/14 8:43
# @Author: Matrix
# @Site:
# @File: api_list.py
# @Software: PyCharm
import hashlib
from services.demo.api_demo import ApiDemo

__author__ = 'matrix'

api_demo = ApiDemo()

api_version = {}


def version(v, enable=True):
    """
    Web Api版本注册
    :param v:  版本号
    :param enable:  版本是否停用
    :return:  无
    """
    def _version(aclass):
        if enable:
            api_version[v] = aclass
        return aclass
    return _version


class ApiMethodMeta(type):

    def __new__(mcs, classname, supers, clsdict):
        cls = type.__new__(mcs, classname, supers, clsdict)
        support_methods = getattr(cls, 'support_methods')
        for support_method in support_methods:
            hash_method = 'x_{hash_method}'.format(
                hash_method=hashlib.sha1(support_method.encode('utf-8')).hexdigest())
            setattr(cls, hash_method, support_methods.get(support_method, None))
        return cls

    def __init__(cls, classname, supers, clsdict):
        type.__init__(cls, classname, supers, clsdict)


class ApiMethodBase(metaclass=ApiMethodMeta):
    support_methods = {
        'matrix.api.get-user': {'func': api_demo.get_user},
        'matrix.api.return-err': {'func': api_demo.raise_error}
    }


@version('1.0')
class ApiMethodV10(ApiMethodBase):
    support_methods = {
        'matrix.api.err-func': {'func': api_demo.err_func},
        'matrix.api.instance-func': {'func': api_demo.instance_func},
        'matrix.api.class-func': {'func': ApiDemo.class_method},
        'matrix.api.send-kwargs': {'func': api_demo.send_kwargs},
        'matrix.api.raise-error': {'func': api_demo.raise_error},
        'matrix.api.only-post': {'func': api_demo.raise_error, 'method': ['post']},
        'matrix.api.api-stop': {'func': api_demo.raise_error, 'enable': False}
    }

if __name__ == '__main__':
    api_list = ApiMethodV10.api_methods
    print(api_version)
    print(api_list)

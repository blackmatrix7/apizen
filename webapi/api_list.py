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
        # 遍历父类的方法,获取父类版本的API方法
        all_api_methods = {}
        for super_ in supers:
            if super_ and 'api_methods' in super_.__dict__:
                super_methods = getattr(super_, 'api_methods')
                all_api_methods.update(super_methods)
        cls = type.__new__(mcs, classname, supers, clsdict)
        all_api_methods.update(getattr(cls, 'support_methods'))
        setattr(cls, 'api_methods', all_api_methods)
        return cls


class ApiMethodBase(metaclass=ApiMethodMeta):
    api_methods = {}
    support_methods = {
        'matrix.api.get-user': {'func': api_demo.get_user},
        'matrix.api.return-err': {'func': api_demo.raise_error}
    }


@version('1.0')
class ApiMethodV10(ApiMethodBase):
    support_methods = {
        'matrix.api.err-func': {'func': api_demo.err_func},
        'matrix.api.instance-func': {'func': api_demo.instance_func}
    }

if __name__ == '__main__':
    api_list = ApiMethodV10.api_methods
    print(api_version)
    print(api_list)

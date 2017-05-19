#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/19 上午8:56
# @Author  : Matrix
# @Site    : 
# @File    : version.py
# @Software: PyCharm
import hashlib

__author__ = 'blackmatrix'

allversion = {}


def register(versions):
    allversion.update(
        {versoin[0]: {'model': versoin[1],
                      'enable': versoin[2]
                      } for versoin in versions
         }
    )


class _ApiMethodMeta(type):

    def __new__(mcs, classname, supers, clsdict):
        cls = type.__new__(mcs, classname, supers, clsdict)
        api_methods = getattr(cls, 'api_methods')
        for api_method in api_methods:
            hash_method = 'x_{hash_method}'.format(
                hash_method=hashlib.sha1(api_method.encode('utf-8')).hexdigest())
            setattr(cls, hash_method, api_methods.get(api_method, None))
        return cls

    def __init__(cls, classname, supers, clsdict):
        type.__init__(cls, classname, supers, clsdict)


class ApiMethodBase(metaclass=_ApiMethodMeta):
    api_methods = {}


if __name__ == '__main__':
    pass

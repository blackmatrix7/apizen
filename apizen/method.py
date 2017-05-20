#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/19 上午9:33
# @Author  : Matrix
# @Site    : 
# @File    : method.py
# @Software: PyCharm
import hashlib
from apizen.error import ApiSysError
from apizen.version import allversion
__author__ = 'blackmatrix'


def get_api_method(version, method_name, request_method):

        # hash方法名
        _hash_method = 'zen_{hash_method}'.format(
            hash_method=hashlib.sha1(method_name.encode('utf-8')).hexdigest())

        # 检查方法名是否存在
        if not hasattr(allversion[version]['methods'], _hash_method):
            raise ApiSysError.invalid_method
        # 检查方法是否停用
        elif not getattr(allversion[version]['methods'], _hash_method).get('enable', True):
            raise ApiSysError.api_stop
        # 检查方法是否允许以某种请求方式调用
        elif request_method.lower() not in \
                getattr(allversion[version]['methods'], _hash_method).get('method', ['get', 'post']):
            raise ApiSysError.not_allowed_request
        # 检查函数是否可调用
        elif not callable(getattr(allversion[version]['methods'], _hash_method).get('func')):
            raise ApiSysError.error_api_config

        return getattr(allversion[version]['methods'], _hash_method).get('func')


class ApiMethod:

    def __init__(self, name, func, method=('get', 'post'), enable=True, auth=False):
        self.name = name
        self.func = func
        self.method = method
        self.enable = enable
        self.auth = auth

if __name__ == '__main__':
    pass

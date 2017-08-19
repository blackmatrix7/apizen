#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/5/28 21:49
# @Author : BlackMatrix
# @Site :
# @File : __init__.py
# @Software: PyCharm
from functools import wraps
from .manager import apizen, ApiZenManager
from .method import get_method, run_method

__all__ = [
    ApiZenManager.__name__,
    'get_method',
    'run_method'
]


def apiconfig(raw_resp=False):
    def _apiconfig(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.raw_resp = raw_resp
        return wrapper
    return _apiconfig


__author__ = 'blackmatrix'

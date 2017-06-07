#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/6/7 下午9:49
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: controller.py
# @Software: PyCharm
from .controller import *
from ..apizen.version import ApiMethodsBase

__author__ = 'blackmatix'


class UserApiMethods(ApiMethodsBase):

    api_methods = {
        # 用户登录
        'apizen.session.get': {'func': user_login, 'methods': ['get']},
        # 获取用户信息
        'apizen.user.get': {'func': None}
    }

if __name__ == '__main__':
    pass

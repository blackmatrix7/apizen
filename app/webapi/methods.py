# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/3/14 8:43
# @Author: BlackMatrix
# @Site:
# @File: controller.py
# @Software: PyCharm
from ..apizen.version import version
from ..user.methods import UserApiMethods
from ..demo.methods import DemoApiMethods

__author__ = 'blackmatrix'


@version(1.0)
class ApiMethodsV10(UserApiMethods, DemoApiMethods):
    api_methods = {}


@version(1.1)
class ApiMethodsV11(ApiMethodsV10):
    api_methods = {}


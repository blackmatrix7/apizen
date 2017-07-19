#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 21:47
# @Author  : BlackMatrix
# @Site    : https://github.com/blackmatrix7
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint
from app.apizen.version import register
from app.demo.methods import DemoApiMethods
from app.webapi.methods import ApiMethodsV10, ApiMethodsV11

__author__ = 'blackmatix'
# 创建蓝图
webapi = Blueprint('webapi', __name__)
# Web Api 版本注册
register(DemoApiMethods)  # 用于测试版本已停用的情况
register(ApiMethodsV10, ApiMethodsV11)

# 必须注册完蓝图后才能导入
from app.webapi import routing

if __name__ == '__main__':
    pass

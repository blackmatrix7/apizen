#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/6/7 下午11:52
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: flaskext.py
# @Software: PyCharm
from flask import Blueprint
from decimal import Decimal
from datetime import datetime
from flask.json import JSONEncoder

__author__ = 'blackmatix'


class ApiZen:

    @staticmethod
    def init_app(app):
        datetime_format = app.config.get('APIZEN_DATETIME_FORMAT', '%Y/%m/%d %H:%M:%S')
        ApiZenJSONEncoder.datetime_format = datetime_format
        app.json_encoder = ApiZenJSONEncoder


class ApiZenJSONEncoder(JSONEncoder):

    datetime_format = None

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime(ApiZenJSONEncoder.datetime_format)
            elif isinstance(obj, Decimal):
                # 不转换为float是为了防止精度丢失
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


# 创建蓝图
webapi = Blueprint('webapi', __name__)
# Web Api 版本注册
# register(DemoApiMethods)  # 用于测试版本已停用的情况
# register(ApiMethodsV10, ApiMethodsV11)

# 必须注册完蓝图后才能导入
from .routing import *

if __name__ == '__main__':
    pass

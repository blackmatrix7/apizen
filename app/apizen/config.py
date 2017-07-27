#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/7/26 21:41
# @Author  : BlackMatrix
# @Site : 
# @File : config.py
# @Software: PyCharm

"""
此模块提供ApiZen配置默认值

ApiZen提供一个默认的接口路由，默认为激活状态。
通过配置文件可以进行关闭。
如果不激活默认接口路由，则以下配置无效：
APIZEN_ROUTE、APIZEN_RESP_FMT
"""

# 是否激活ApiZen默认的路由
ACTIVATE_DEFAULT_ROUTE = True

# 接口路由默认地址
APIZEN_ROUTE = ('/api/router/rest', '/api/router/json')

# 接口默认返回格式
APIZEN_RESP_FMT = '{"meta": {"code": {code}, "message": {message}}, "response": {response}}'

# 接口版本位置
APIZEN_VERSIONS = None

# 默认Date格式
APIZEN_DATE_FMT = '%Y/%m/%d'

# 默认DateTime格式
APIZEN_DATETIME_FMT = '%Y/%m/%d %H:%M:%S'


__author__ = 'blackmatrix'

if __name__ == '__main__':
    pass


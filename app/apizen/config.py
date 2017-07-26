#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/7/26 21:41
# @Author  : BlackMatrix
# @Site : 
# @File : config.py
# @Software: PyCharm

"""
此模块提供ApiZen配置默认值
"""

# 接口路由默认地址
APIZEN_ROUTE = ('/api/router/rest', '/api/router/json')

# 接口版本位置
APIZEN_VERSIONS = (None, )

# 默认Date格式
APIZEN_DATE_FMT = '%Y/%m/%d'

# 默认DateTime格式
APIZEN_DATETIME_FMT = '%Y/%m/%d %H:%M:%S'

# 接口默认返回格式
APIZEN_RESP_FMT = '{"meta": {"code": {code}, "message": {message}}, "response": {response}}'

__author__ = 'blackmatrix'

if __name__ == '__main__':
    pass


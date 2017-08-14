#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/7/26 21:41
# @Author  : BlackMatrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : config.py
# @Software: PyCharm

"""
-------------------------------
ApiZen 接口版本的注册、管理与继承功能
-------------------------------
适用版本：Flask，Tornado
-------------------------------
其他说明：

ApiZen提供一个默认的接口路由，默认为激活状态。
通过配置文件可以进行关闭。
如果不激活默认接口路由，则以下配置无效：
APIZEN_ROUTE、APIZEN_RESP_FMT
"""

__author__ = 'blackmatrix'


class ConfigMixin:

    def __setitem__(self, key, value):
        raise AttributeError

    def __delitem__(self, key):
        raise AttributeError

    def __getitem__(self, item):
        return getattr(self, item)

    def items(self):
        yield from {k: getattr(self, k, None) for k in dir(self) if k.upper() == k}.items()

    def get(self, item, value=None):
        return getattr(self, item, value)


class BaseConfig(ConfigMixin):
    pass


class DefaultConfig(BaseConfig):

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


default_config = DefaultConfig()

current_config = {}


def set_current_config(key, value):
    current_config[key] = value

if __name__ == '__main__':
    pass


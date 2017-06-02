# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/3/14 8:43
# @Author: BlackMatrix
# @Site:
# @File: methods.py
# @Software: PyCharm
from app.apizen.version import ApiMethodsBase, version
from app.webapi.services.demo import demo

__author__ = 'blackmatrix'


@version(1.0)
class ApiMethodsV10(ApiMethodsBase):
    api_methods = {
        # 第一个demo
        'matrix.api.set-user': {'func': demo.set_user},
        # 以list的方式传值
        'matrix.api.set-users': {'func': demo.set_users},
        # 操作数据库
        'matrix.api.set-client': {'func': demo.set_client},
        # 抛出一个异常
        'matrix.api.return-err': {'func': demo.raise_error},
        # 错误的函数编写
        'matrix.api.err-func': {'func': demo.err_func},
        # 实例方法调用
        'matrix.api.instance-func': {'func': demo.instance_func},
        # 类方法调用
        'matrix.api.class-func': {'func': demo.class_method}
    }


@version(1.1)
class ApiMethodsV11(ApiMethodsV10):
    api_methods = {
        # 传递任意参数
        'matrix.api.send-kwargs': {'func': demo.send_kwargs},
        # API版本继承
        'matrix.api.raise-error': {'func': demo.raise_error}
    }


@version(1.2)
class ApiMethodsV12(ApiMethodsV11):
    api_methods = {
        # 只允许POST请求
        'matrix.api.only-post': {'func': demo.raise_error, 'methods': ['post']},
        # 停用API
        'matrix.api.api-stop': {'func': demo.raise_error, 'enable': False},
        # 自定义一个异常信息
        'matrix.api.custom-error': {'func': demo.custom_error}
    }


if __name__ == '__main__':
    api_list = ApiMethodsV10.api_methods
    print(api_list)

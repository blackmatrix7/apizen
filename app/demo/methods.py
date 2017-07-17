#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/6/7 下午9:52
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: methods.py
# @Software: PyCharm
from .controller import *
from ..apizen.version import ApiMethodsBase, version

__author__ = 'blackmatrix'


@version('demo', enable=False)
class DemoApiMethods(ApiMethodsBase):
    api_methods = {
        # 第一个API
        'matrix.api.first-api': {'func': first_api},
        # 接口参数自动判断
        'matrix.api.register_user': {'func': register_user},
        # 接口参数类型自动判断
        'matrix.api.register_user_plus': {'func': register_user_plus},
        # 自定义类型判断方式
        'matrix.api.validate_email': {'func': validate_email},
        # JSON 转 Dict
        'matrix.api.json-to-dict': {'func': json_to_dict},
        # JSON 转 List
        'matrix.api.json-to-list': {'func': json_to_list},
        # 抛出一个异常
        'matrix.api.return-err': {'func': raise_error},
        # 自定义一个异常信息
        'matrix.api.custom-error': {'func': custom_error},
        # 保留原始返回格式
        'matrix.api.raw_response': {'func': raw_data},
        # 只允许GET请求
        'matrix.api.only-get': {'func': first_api, 'methods': ['get']},
        # 只允许POST请求
        'matrix.api.only-post': {'func': first_api, 'methods': ['post']},
        # 允许post和get
        'matrix.api.get-post': {'func': first_api},
        # 停用API
        'matrix.api.api-stop': {'func': first_api, 'enable': False},
        # 错误的API配置
        'matrix.api.err-api': {'func': first_api()},
        # 错误的函数编写
        'matrix.api.err-func': {'func': demo.err_func},
        # 实例方法调用
        'matrix.api.instance-func': {'func': demo.instance_func},
        # 类方法调用
        'matrix.api.class-func': {'func': demo.class_method},
        # 传递任意参数
        'matrix.api.send-kwargs': {'func': demo.send_kwargs},
        # API版本继承
        'matrix.api.raise-error': {'func': raise_error},
        # 保存到数据库
        'matrix.api.save-db': {'func': save_to_db}
    }

if __name__ == '__main__':
    pass

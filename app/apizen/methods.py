#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/19 上午9:33
# @Author  : Matrix
# @Site    : 
# @File    : controller.py
# @Software: PyCharm
import copy
import json
from functools import wraps
from inspect import Signature, unwrap
from .version import allversion
from json import JSONDecodeError
from inspect import signature, Parameter
from .exceptions import ApiSysExceptions

__author__ = 'blackmatrix'

'''
接口处理方法的异常判断与执行
'''


def do_not_format(func):
    """
    装饰器，表示接口处理函数返回的值不需要统一的返回格式
    :param func: 装饰的函数
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper.format_retinfo = False
    return wrapper


class Method:

    @staticmethod
    def convert(key, value, default_value, type_hints):
        converter = {
                    'int': lambda: int(_arg_value) if isinstance(value, str) else _arg_value,
                    'float': lambda: float(_arg_value),
                    'str': lambda: str(_arg_value),
                    'list': lambda: json.loads(_arg_value) if isinstance(value, str) else _arg_value,
                    'dict': lambda: json.loads(_arg_value) if isinstance(value, str) else _arg_value,
                    'tuple': lambda: tuple(json.loads(_arg_value) if isinstance(value, str) else _arg_value)
                }
        try:
            _arg_value = copy.copy(value)
            type_hints_name = type_hints.__name__.lower()
            if _arg_value != default_value \
                    and type_hints != Parameter.empty \
                    and type_hints_name in converter:
                _arg_value = converter[type_hints_name]()
                if not isinstance(_arg_value, type_hints):
                    raise ValueError
        # JSONDecodeError是ValueError的子类
        # 如果不先做解析异常的判断，会显示参数类型错误，虽然看起来也没什么不对
        except JSONDecodeError:
            raise ApiSysExceptions.invalid_json
        except ValueError:
            api_ex = ApiSysExceptions.error_args_type
            api_ex.message = '{0}：{1} <{2}>'.format(ApiSysExceptions.error_args_type.message, key, type_hints.__name__)
            raise api_ex
        else:
            return _arg_value

    # 获取api处理函数及相关异常判断
    @staticmethod
    def get(version, method_name, request_method):

            """
            获取api处理函数及相关异常判断
            :param version:  接口版本
            :param method_name:  方法名
            :param request_method:  http请求方式
            :return: 
            """
            format_retinfo = True
            allow_anonymous = False

            def check_decorator(func):
                nonlocal format_retinfo
                nonlocal allow_anonymous
                if hasattr(func, 'format_retinfo') and func.format_retinfo is False:
                    format_retinfo = False
                if hasattr(func, 'allow_anonymous') and func.allow_anonymous is True:
                    allow_anonymous = True

            # 检查版本号
            if version not in allversion:
                raise ApiSysExceptions.unsupported_version
            # 检查版本是否停用
            elif not allversion[version].get('enable', True):
                raise ApiSysExceptions.version_stop

            methods = getattr(allversion[version]['methods'], 'api_methods')

            # 检查方法名是否存在
            if method_name not in methods:
                raise ApiSysExceptions.invalid_method
            # 检查方法是否停用
            elif not methods[method_name].get('enable', True):
                raise ApiSysExceptions.api_stop
            # 检查方法是否允许以某种请求方式调用
            elif request_method.lower() not in methods[method_name].get('methods', ['get', 'post']):
                raise ApiSysExceptions.not_allowed_request
            # 检查函数是否可调用
            elif not callable(methods[method_name].get('func')):
                raise ApiSysExceptions.error_api_config

            _func = methods[method_name].get('func')

            # 解包，检查是否有不统一格式化输出的装饰器，或运行匿名访问情况
            unwrap(_func, stop=check_decorator)

            return _func, format_retinfo, allow_anonymous

    # 运行接口处理方法，及异常处理
    @staticmethod
    def run(api_method, request_params):

        # 最终传递给接口处理方法的全部参数
        func_args = {}
        if hasattr(api_method, 'format_retinfo') and api_method.format_retinfo:
            print(True)
        # 获取函数方法的参数
        api_method_params = signature(api_method).parameters

        for k, v in api_method_params.items():
            if str(v.kind) == 'VAR_POSITIONAL':
                raise ApiSysExceptions.error_api_config
            elif str(v.kind) in ('POSITIONAL_OR_KEYWORD', 'KEYWORD_ONLY'):
                if k not in request_params:
                    if v.default is Parameter.empty:
                        missing_arguments = ApiSysExceptions.missing_arguments
                        missing_arguments.message = '{0}：{1}'.format(missing_arguments.message, k)
                        raise missing_arguments
                    func_args[k] = Method.convert(k, v.default, v.default, v.annotation)
                else:
                    func_args[k] = Method.convert(k, request_params.get(k), v.default, v.annotation)
            elif str(v.kind) == 'VAR_KEYWORD':
                func_args.update({k: v for k, v in request_params.items()
                                  if k not in api_method_params.keys()})
        return api_method(**func_args)

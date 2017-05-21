#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/19 上午9:33
# @Author  : Matrix
# @Site    : 
# @File    : method.py
# @Software: PyCharm
import json
import copy
from json import JSONDecodeError
from apizen.version import allversion
from inspect import signature, Parameter
from apizen.error import ApiError, ApiSysError
__author__ = 'blackmatrix'

'''
接口处理方法的异常判断与执行
'''


# 获取api处理函数及相关异常判断
def get_api_method(version, method_name, request_method):

        """
        获取api处理函数及相关异常判断
        :param version:  接口版本
        :param method_name:  方法名
        :param request_method:  http请求方式
        :return: 
        """

        # 检查版本号
        if version not in allversion:
            raise ApiSysError.unsupported_version
        elif not allversion[version].get('enable', True):
            raise ApiSysError.version_stop

        methods = getattr(allversion[version]['methods'], 'api_methods')

        # 检查方法名是否存在
        if method_name not in methods:
            raise ApiSysError.invalid_method
        # 检查方法是否停用
        elif not methods[method_name].get('enable', True):
            raise ApiSysError.api_stop
        # 检查方法是否允许以某种请求方式调用
        elif request_method.lower() not in methods[method_name].get('method', ['get', 'post']):
            raise ApiSysError.not_allowed_request
        # 检查函数是否可调用
        elif not callable(methods[method_name].get('func')):
            raise ApiSysError.error_api_config

        return methods[method_name].get('func')


# 运行接口处理方法
def _run_api_method(version, method_name, request_method, request_params):

    # 最终传递给接口处理方法的全部参数
    func_args = {}

    # 使用Type Hints判断接口处理方法限制的参数类型
    def set_method_args(arg_key, arg_value, default_value, type_hints):
        _arg_value = copy.copy(arg_value)
        try:
            converter = {
                'int': lambda: int(_arg_value) if isinstance(arg_value, str) else _arg_value,
                'float': lambda: float(_arg_value),
                'str': lambda: str(_arg_value),
                'list': lambda: json.loads(_arg_value) if isinstance(arg_value, str) else _arg_value,
                'dict': lambda: json.loads(_arg_value) if isinstance(arg_value, str) else _arg_value,
                'tuple': lambda: tuple(json.loads(_arg_value) if isinstance(arg_value, str) else _arg_value)
            }
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
            raise ApiSysError.invalid_json
        except ValueError:
            api_ex = ApiSysError.error_args_type
            api_ex.message = '{0}：{1} <{2}>'.format(ApiSysError.error_args_type.message, arg_key, type_hints.__name__)
            raise api_ex
        else:
            func_args[arg_key] = _arg_value

    # 获取接口处理方法
    api_method = get_api_method(version=version,
                                method_name=method_name,
                                request_method=request_method)

    # 获取函数方法的参数
    api_method_params = signature(api_method).parameters

    for k, v in api_method_params.items():
        if str(v.kind) == 'VAR_POSITIONAL':
            raise ApiSysError.error_api_config
        elif str(v.kind) in ('POSITIONAL_OR_KEYWORD', 'KEYWORD_ONLY'):
            if k not in request_params:
                if v.default is Parameter.empty:
                    missing_arguments = ApiSysError.missing_arguments
                    missing_arguments.message = '{0}：{1}'.format(missing_arguments.message, k)
                    raise missing_arguments
                set_method_args(k,  v.default, v.default, v.annotation)
            else:
                value = request_params.get(k)
                set_method_args(k, value, v.default, v.annotation)
        elif str(v.kind) == 'VAR_KEYWORD':
            func_args.update({k: v for k, v in request_params.items()
                              if k not in api_method_params.keys()})

    return api_method(**func_args)


# 运行接口处理方法，及异常处理
def run_api_method(version, method_name, request_method, request_params):

    try:
        result = _run_api_method(version=version,
                                 method_name=method_name,
                                 request_method=request_method,
                                 request_params=request_params)
    except ApiError as ex:
        raise ex
    except JSONDecodeError:
        raise ApiSysError.invalid_json
    except Exception as ex:
        api_ex = ApiSysError.system_error
        api_ex.message = '{0}：{1}'.format(api_ex.message, ex)
        raise api_ex
    return result


if __name__ == '__main__':
    pass

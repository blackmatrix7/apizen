#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/19 上午9:33
# @Author  : Matrix
# @Site    : 
# @File    : method.py
# @Software: PyCharm
import json
import copy
import hashlib
from json import JSONDecodeError
from apizen.version import allversion
from inspect import signature, Parameter
from apizen.error import ApiError, ApiSysError
__author__ = 'blackmatrix'


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

        # hash方法名
        _hash_method = 'zen_{hash_method}'.format(
            hash_method=hashlib.sha1(method_name.encode('utf-8')).hexdigest())

        # 检查方法名是否存在
        if not hasattr(allversion[version]['methods'], _hash_method):
            raise ApiSysError.invalid_method
        # 检查方法是否停用
        elif not getattr(allversion[version]['methods'], _hash_method).get('enable', True):
            raise ApiSysError.api_stop
        # 检查方法是否允许以某种请求方式调用
        elif request_method.lower() not in \
                getattr(allversion[version]['methods'], _hash_method).get('method', ['get', 'post']):
            raise ApiSysError.not_allowed_request
        # 检查函数是否可调用
        elif not callable(getattr(allversion[version]['methods'], _hash_method).get('func')):
            raise ApiSysError.error_api_config

        return getattr(allversion[version]['methods'], _hash_method).get('func')


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
            message = '{0}：{1} <{2}>'.format(ApiSysError.error_args_type.message, arg_key, type_hints.__name__)
            api_ex = ApiBaseError(
                err_code=ApiSysError.error_args_type.err_code,
                status_code=ApiSysError.error_args_type.status_code,
                message=message)
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
            # 当没有默认值且没有传入参数时，必须抛出参数缺失的异常
            if k not in request_params and v.default is Parameter.empty:
                api_ex = ApiSysError.missing_arguments
                api_ex.message = '{0}：{1}'.format(api_ex.message, k)
                raise api_ex
            else:
                value = request_params.get(k)
                set_method_args(k, value, v.default, v.annotation)
        elif str(v.kind) == 'VAR_KEYWORD':
            func_args.update({k: v for k, v in request_params.items()
                              if k not in api_method_params.keys()})
    return api_method(**func_args)


# 运行接口处理方法，及异常处理
def run_api_method(version, method_name, request_method, request_params):

    # 接口处理方法执行结果
    result = None
    # http status code
    status_code = 200
    # api code
    api_code = 1000
    # 执行消息
    api_msg = '执行成功'

    try:
        _run_api_method(version=version,
                        method_name=method_name,
                        request_method=request_method,
                        request_params=request_params)
    except JSONDecodeError:
        api_ex = ApiSysError.invalid_json
        api_code = api_ex.err_code
        status_code = api_ex.status_code
        api_msg = api_ex.message
    # API其他异常
    except ApiError as api_ex:
        api_code = api_ex.err_code
        status_code = api_ex.status_code
        api_msg = api_ex.message
    # 全局异常
    except Exception as ex:
        api_ex = ApiSysError.system_error
        api_code = api_ex.err_code
        status_code = api_ex.status_code
        api_msg = '{0}：{1}'.format(api_ex.message, ex)
    finally:
        return result, status_code, api_code, api_msg


class ApiMethod:

    def __init__(self, name, func, method=('get', 'post'), enable=True, auth=False):
        self.name = name
        self.func = func
        self.method = method
        self.enable = enable
        self.auth = auth

if __name__ == '__main__':
    pass
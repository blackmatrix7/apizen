#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/5 下午3:29
# @Author  : Matrix
# @Site    : 
# @File    : api_route.py
# @Software: PyCharm
import json
import copy
import hashlib
from json import JSONDecodeError
from apizen.error import ApiSysError
from apizen.version import allversion
from inspect import signature, Parameter
from webapi.api_base import ApiBaseHandler
from webapi.api_error import ApiBaseError

__author__ = 'matrix'


class WebApiRoute(ApiBaseHandler):

    def call_api_func(self):

        # 接口名称
        self._method = self.get_argument('method')
        # 接口版本
        self._v = self.get_argument('v')
        # 数据格式
        self._format = self.get_argument('format', 'json').lower()
        # access_token
        self._access_token = self.get_argument('access_token', None)
        # app_key
        self._app_key = self.get_argument('app_key', None)
        # 签名
        self._sign = self.get_argument('sign', None)
        # 时间戳
        self._timestamp = self.get_argument('timestamp', None)

        # 检查请求的格式
        if self._format not in ('json', 'xml'):
            raise ApiSysError.invalid_format

        # 检查版本号
        if self._v not in allversion:
            raise ApiSysError.unsupported_version

        # hash方法名
        _hash_method = 'x_{hash_method}'.format(
            hash_method=hashlib.sha1(self._method.encode('utf-8')).hexdigest())

        # 检查方法名是否存在
        if not hasattr(allversion[self._v]['model'], _hash_method):
            raise ApiSysError.invalid_method
        # 检查方法是否停用
        elif not getattr(allversion[self._v]['model'], _hash_method).get('enable', True):
            raise ApiSysError.api_stop
        # 检查方法是否允许以某种请求方式调用
        elif self.request.method.lower() not in \
                getattr(allversion[self._v]['model'], _hash_method).get('method', ['get', 'post']):
            raise ApiSysError.not_allowed_request

        # 使用Type Hints判断接口处理函数限制的参数类型
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

        # 函数参数
        func_args = {}

        # 请求参数
        content_type = self.request.headers['Content-Type'].lower() if 'Content-Type' in self.request.headers else None
        request_args = {key: self.get_argument(key) for key in self.request.arguments}

        if content_type == 'application/json':
            body_data = json.loads(self.request.body.decode())
            if body_data and isinstance(body_data, dict):
                request_args.update(body_data)
            else:
                raise ApiSysError.invalid_json

        # 获取函数对象
        method_func = getattr(allversion[self._v]['model'], _hash_method).get('func', None)
        # 检查函数对象是否有效
        if not callable(method_func):
            raise ApiSysError.error_api_config
        # 获取函数参数
        func_param = signature(method_func).parameters

        for k, v in func_param.items():
            if str(v.kind) == 'VAR_POSITIONAL':
                raise ApiSysError.error_api_config
            elif str(v.kind) in ('POSITIONAL_OR_KEYWORD', 'KEYWORD_ONLY'):
                value = request_args.get(k) if k in request_args else v.default if v.default != Parameter.empty else self.get_argument(k)
                set_method_args(k, value, v.default, v.annotation)
            elif str(v.kind) == 'VAR_KEYWORD':
                func_args.update({k: v for k, v in request_args.items()
                                  if k not in func_param.keys()})

        return method_func(**func_args)

    def get(self):
        self.format_retinfo()

    def post(self):
        self.format_retinfo()


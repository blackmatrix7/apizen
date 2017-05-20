#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/5 下午3:29
# @Author  : Matrix
# @Site    : 
# @File    : api_route.py
# @Software: PyCharm
import json
from apizen.error import ApiSysError
from apizen.method import run_api_method
from webapi.api_base import ApiBaseHandler
__author__ = 'blackmatrix'


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

        # TODO 判断参数缺失的异常怎么办

        # 拼装请求参数
        content_type = self.request.headers['Content-Type'].lower() if 'Content-Type' in self.request.headers else None
        request_args = {key: self.get_argument(key) for key in self.request.arguments}

        if content_type == 'application/json':
            body_data = json.loads(self.request.body.decode())
            if body_data and isinstance(body_data, dict):
                request_args.update(body_data)
            else:
                raise ApiSysError.invalid_json

        return run_api_method(version=self._v, method_name=self._method, request_method=self.request.method, request_params=request_args)

    def get(self):
        self.format_retinfo()

    def post(self):
        self.format_retinfo()


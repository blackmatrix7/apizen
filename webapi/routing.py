#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/5 下午3:29
# @Author  : Matrix
# @Site    : 
# @File    : routing.py
# @Software: PyCharm
import json
from dict2xml import dict2xml
from json import JSONDecodeError
from apizen.method import Method
from webapi.handler import ApiBaseHandler
from tornado.web import MissingArgumentError
from apizen.exception import ApiException, ApiSysExceptions

__author__ = 'blackmatrix'


class WebApiRoute(ApiBaseHandler):

    def handler(self):

        result = None
        api_code = 1000
        api_msg = '执行成功'
        http_code = 200

        try:
            result = self.call_api_func()
        # 参数缺失异常
        except KeyError:
            api_code = 2000
            http_code = 500
            api_msg = '抓到你了'
        # 参数缺失异常
        except MissingArgumentError as miss_arg_err:
            # 缺少方法名
            if miss_arg_err.arg_name == 'method':
                api_ex = ApiSysExceptions.missing_method
            # 缺少版本号
            elif miss_arg_err.arg_name == 'v':
                api_ex = ApiSysExceptions.missing_version
            # 其他缺少参数的情况
            else:
                api_ex = ApiSysExceptions.missing_arguments
            api_msg = '{0}:{1}'.format(api_ex.message, miss_arg_err.arg_name)
            api_code = api_ex.err_code
            http_code = api_ex.status_code
        # JSON解析异常
        except JSONDecodeError:
            api_ex = ApiSysExceptions.invalid_json
            api_code = api_ex.err_code
            http_code = api_ex.status_code
            api_msg = api_ex.message
        # API其他异常
        except ApiException as api_ex:
            api_code = api_ex.err_code
            http_code = api_ex.status_code
            api_msg = api_ex.message
        # 全局异常
        except Exception as ex:
            api_ex = ApiSysExceptions.system_error
            api_code = api_ex.err_code
            http_code = api_ex.status_code
            api_msg = '{0}：{1}'.format(api_ex.message, ex)

        retinfo = {
            'meta': {
                'code': api_code,
                'message': api_msg
            },
            'respone': result
        }

        if self._format == 'xml':
            retinfo = dict2xml(retinfo)

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_status(status_code=http_code)
        self.write(retinfo)

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
            raise ApiSysExceptions.invalid_format

        # 拼装请求参数
        content_type = self.request.headers['Content-Type'].lower() if 'Content-Type' in self.request.headers else None
        request_args = {key: self.get_argument(key) for key in self.request.arguments}

        if content_type == 'application/json' and self.request.method.lower() == 'post':
            body_data = json.loads(self.request.body.decode())
            if body_data and isinstance(body_data, dict):
                request_args.update(body_data)
            else:
                raise ApiSysExceptions.invalid_json

        return Method.run(version=self._v, method_name=self._method, request_method=self.request.method, request_params=request_args)

    def get(self):
        self.handler()

    def post(self):
        self.handler()


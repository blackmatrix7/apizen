# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2017/1/5 10:23
# Author: Matrix
# Site:
# File: base.py
# Software: PyCharm
from dict2xml import dict2xml
from tornado.web import RequestHandler
from webapi.api_error import ApiBaseError, ApiSysError


class BaseHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    def set_default_headers(self):
        pass


class SysBaseHandler(BaseHandler):
    pass


class ApiBaseHandler(SysBaseHandler):

    def call_api_func(self):
        pass

    def format_retinfo(self):

        result_code = 1000
        message = '执行成功'
        result = None
        status_code = 200

        try:
            result = self.call_api_func()
        except ApiBaseError as api_ex:
            result_code = api_ex.err_code
            status_code = api_ex.status_code
            message = api_ex.message
        except Exception as ex:
            api_ex = ApiSysError.system_error
            result_code = api_ex.err_code
            status_code = api_ex.status_code
            message = '{0}：{1}'.format(api_ex.message, ex)

        retinfo = {
            'meta': {
                'code': result_code,
                'message': message
            },
            'respone': result
        }

        if self._format == 'xml':
            retinfo = dict2xml(retinfo)

        self.set_status(status_code=status_code)
        self.write(retinfo)

    def __init__(self, application, request, **kwargs):
        self._access_token = None
        self._method = None
        self._app_key = None
        self._sign = None
        self._timestamp = None
        self._v = None
        self._format = 'json'
        SysBaseHandler.__init__(self, application, request, **kwargs)


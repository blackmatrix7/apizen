#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/16 上午11:20
# @Author  : Matrix
# @Site    : 
# @File    : api_base.py
# @Software: PyCharm
from dict2xml import dict2xml
from json import JSONDecodeError
from handler.base import SysBaseHandler
from tornado.web import MissingArgumentError
from webapi.api_error import ApiBaseError, ApiSysError

__author__ = 'blackmatrix'


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
        except MissingArgumentError as miss_arg_err:
            api_ex = ApiSysError.missing_arguments
            result_code = api_ex.err_code
            status_code = api_ex.status_code
            message = '{message}:{arg_name}'.format(
                message=ApiSysError.missing_arguments.message,
                arg_name=miss_arg_err.arg_name)
        except JSONDecodeError:
            api_ex = ApiSysError.invalid_json
            result_code = api_ex.err_code
            status_code = api_ex.status_code
            message = api_ex.message
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


if __name__ == '__main__':
    pass

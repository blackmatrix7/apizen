# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/3/14 9:56
# @Author: Matrix
# @Site: http://www.vcansenior.com
# @File: api_retinfo.py
# @Software: PyCharm
from functools import wraps
from dict2xml import dict2xml
from webapi.api_error import ApiSysError, ApiBaseError

__author__ = 'matrix'


def api_retinfo(func):

    @wraps(func)
    def _webapi(*args, **kwargs):
        self = args[0]

        result_code = 1000
        message = '执行成功'
        result = None
        status_code = 200
        format_ = 'json'

        try:
            result, format_ = func(*args, **kwargs)
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

        if format_ == 'xml':
            retinfo = dict2xml(data=retinfo)

        self.set_status(status_code=status_code)
        self.write(retinfo)

    return _webapi

if __name__ == '__main__':
    pass


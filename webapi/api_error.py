#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/12 下午9:46
# @Author  : Matrix
# @Site    : 
# @File    : api_error.py
# @Software: PyCharm
from apizen.error import ApiBaseError


# API 子系统（业务）层级执行结果，以2000开始
class ApiSubError:
    empty_result = ApiBaseError(err_code=2000, status_code=200, message='查询结果为空')
    unknown_error = ApiBaseError(err_code=2001, status_code=500, message='未知异常')
    other_error = ApiBaseError(err_code=2002, status_code=500, message='其它异常')

if __name__ == '__main__':
    pass

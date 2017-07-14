#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/12 下午9:46
# @Author  : Matrix
# @Site    : 
# @File    : exceptions.py
# @Software: PyCharm
from app.apizen.exceptions import ApiException


# API 子系统（业务）层级执行结果，以2000开始
class ApiSubExceptions:
    empty_result = ApiException(err_code=2000, http_code=200, err_msg='查询结果为空', err_type=Exception)
    unknown_error = ApiException(err_code=2001, http_code=500, err_msg='未知异常', err_type=Exception)
    other_error = ApiException(err_code=2002, http_code=500, err_msg='其它异常', err_type=Exception)
    user_not_exits = ApiException(err_code=2003, http_code=404, err_msg='用户不存在', err_type=Exception)
    wrong_password = ApiException(err_code=2004, http_code=400, err_msg='用户名或密码错误', err_type=Exception)
    email_registered = ApiException(err_code=2005, http_code=400, err_msg='邮箱已注册', err_type=Exception)

if __name__ == '__main__':
    pass

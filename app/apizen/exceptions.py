#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/19 上午8:54
# @Author  : Matrix
# @Site    : 
# @File    : exceptions.py
# @Software: PyCharm
import types
from json import JSONDecodeError

__author__ = 'blackmatrix'

'''
接口异常类型的管理与继承
'''

_no_value = object()


class ZenException(Exception):

    def __init__(self, err_msg, err_code='0000', http_code=500):
        self.err_msg = err_msg
        self.err_code = err_code
        self.http_code = http_code

    def __str__(self):
        return str('异常编号：{err_code} 异常信息：{err_msg}'.format(
            err_code=self.err_code,
            err_msg=self.err_msg))

    # 让类实例变成可调用对象，用于接收自定义异常信息，并抛出
    def __call__(self, err_msg=_no_value, *, err_code=_no_value, http_code=_no_value):
        if err_msg is not _no_value:
            self.err_msg = err_msg
        if err_code is not _no_value:
            self.err_code = err_code
        if http_code is not _no_value:
            self.http_code = http_code
        return self


class ApiException:

    def __init__(self, err_code, err_msg, http_code, err_type=Exception):
        self.err_msg = err_msg
        self.ex_type = err_type
        self.err_code = err_code
        self.http_code = http_code

    def __set__(self, instance, value):
        raise AttributeError('禁止修改异常设定')

    def __get__(self, instance, owner):
        supers = (ZenException, self.ex_type, Exception) \
            if self.ex_type and self.ex_type is not Exception else (ZenException, Exception)
        api_ex_cls = types.new_class('ApiException', supers, {}, lambda ns: ns)
        api_ex = api_ex_cls(err_msg=self.err_msg, err_code=self.err_code, http_code=self.http_code)
        return api_ex
    

# API 系统层面异常信息
class ApiSysExceptions:
    # code 1000 为保留编码，代表执行成功，异常信息以1001开始
    # 服务不可用
    missing_system_error = ApiException(err_code=1001, http_code=403, err_msg='服务不可用', err_type=Exception)
    # 限制时间内调用失败次数
    app_call_limited = ApiException(err_code=1002, http_code=403, err_msg='限制时间内调用失败次数', err_type=Exception)
    # 请求被禁止
    forbidden_request = ApiException(err_code=1003, http_code=403, err_msg='请求被禁止', err_type=Exception)
    # 缺少版本参数
    missing_version = ApiException(err_code=1004, http_code=400, err_msg='缺少版本参数', err_type=KeyError)
    # 不支持的版本号
    unsupported_version = ApiException(err_code=1005, http_code=400, err_msg='不支持的版本号', err_type=ValueError)
    # 非法的版本参数
    version_stop = ApiException(err_code=1006, http_code=400, err_msg='接口版本已停用', err_type=ValueError)
    # 缺少时间戳参数
    missing_timestamp = ApiException(err_code=1007, http_code=400, err_msg='缺少时间戳参数', err_type=KeyError)
    # 非法的时间戳参数
    invalid_timestamp = ApiException(err_code=1008, http_code=400, err_msg='非法的时间戳参数', err_type=ValueError)
    # 缺少签名参数
    missing_signature = ApiException(err_code=1009, http_code=400, err_msg='缺少签名参数', err_type=KeyError)
    # 无效签名
    invalid_signature = ApiException(err_code=1010, http_code=400, err_msg='无效签名', err_type=ValueError)
    # 无效数据格式
    invalid_format = ApiException(err_code=1011, http_code=400, err_msg='无效数据格式', err_type=ValueError)
    # 缺少方法名参数
    missing_method = ApiException(err_code=1012, http_code=400, err_msg='缺少方法名参数', err_type=KeyError)
    # 不存在的方法名
    invalid_method = ApiException(err_code=1013, http_code=404, err_msg='不存在的方法名', err_type=AttributeError)
    # 缺少access_token参数
    missing_access_token = ApiException(err_code=1014, http_code=400, err_msg='缺少access_token参数', err_type=KeyError)
    # 无效access_token
    invalid_access_token = ApiException(err_code=1015, http_code=401, err_msg='无效access_token', err_type=ValueError)
    # api已经停用
    api_stop = ApiException(err_code=1016, http_code=405, err_msg='api已经停用', err_type=Exception)
    # 系统处理错误
    system_error = ApiException(err_code=1017, http_code=500, err_msg='系统处理错误', err_type=Exception)
    # 缺少方法所需参数
    missing_arguments = ApiException(err_code=1018, http_code=400, err_msg='缺少方法所需参数', err_type=KeyError)
    # 不支持的http请求方式
    not_allowed_request = ApiException(err_code=1019, http_code=405, err_msg='不支持的http请求方式', err_type=Exception)
    # 错误的API配置
    error_api_config = ApiException(err_code=1020, http_code=500, err_msg='错误的API配置', err_type=NotImplementedError)
    # 无效的json格式
    invalid_json = ApiException(err_code=1021, http_code=400, err_msg='错误或不合法的json格式', err_type=JSONDecodeError)
    # 参数类型错误
    error_args_type = ApiException(err_code=1022, http_code=400, err_msg='参数类型错误', err_type=KeyError)
    # 缺少Content-Type
    missing_content_type = ApiException(err_code=1023, http_code=400, err_msg='缺少Content-Type', err_type=Exception)
    # 不被接受的Content-Type
    unacceptable_content_type = ApiException(err_code=1024, http_code=400, err_msg='不被接受的Content-Type', err_type=Exception)
    # 无效的请求
    bad_request = ApiException(err_code=1025, http_code=400, err_msg='无效的请求', err_type=Exception)

if __name__ == '__main__':
    pass

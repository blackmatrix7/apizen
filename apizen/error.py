#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/19 上午8:54
# @Author  : Matrix
# @Site    : 
# @File    : error.py
# @Software: PyCharm

__author__ = 'blackmatrix'

'''
接口异常类型的管理与继承
'''


class ApiError(Exception):

    def __init__(self, err_code, message, status_code=500):
        self.err_code = err_code
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return str('异常编号：{code}; Http Code:{status_code}; 异常信息：{message}'.format(
            code=self.err_code,
            status_code=self.status_code,
            message=self.message))


class MetaApiError(type):

    def __getattribute__(self, item):
        api_ex = super().__getattribute__(item)
        new_api_ex = ApiError(err_code=api_ex['api_code'],
                              status_code=api_ex['http_code'],
                              message=api_ex['api_msg'])
        return new_api_ex


class ApiBaseError(metaclass=MetaApiError):
    pass


# API 系统层面异常信息，以1000开始
class ApiSysError(ApiBaseError):
    # code 1000 为保留编码，代表执行成功
    # 服务不可用
    missing_system_error = {'api_code': 1001, 'http_code': 403, 'api_msg': '服务不可用'}
    # 限制时间内调用失败次数
    app_call_limited = {'api_code': 1002, 'http_code': 403, 'api_msg': '限制时间内调用失败次数'}
    # 请求被禁止
    forbidden_request = {'api_code': 1003, 'http_code': 403, 'api_msg': '请求被禁止'}
    # 缺少版本参数
    missing_version = {'api_code': 1004, 'http_code': 400, 'api_msg': '缺少版本参数'}
    # 不支持的版本号
    unsupported_version = {'api_code': 1005, 'http_code': 400, 'api_msg': '不支持的版本号'}
    # 非法的版本参数
    version_stop = {'api_code': 1006, 'http_code': 400, 'api_msg': '接口版本已停用'}
    # 缺少时间戳参数
    missing_timestamp = {'api_code': 1007, 'http_code': 400, 'api_msg': '缺少时间戳参数'}
    # 非法的时间戳参数
    invalid_timestamp = {'api_code': 1008, 'http_code': 400, 'api_msg': '非法的时间戳参数'}
    # 缺少签名参数
    missing_signature = {'api_code': 1009, 'http_code': 400, 'api_msg': '缺少签名参数'}
    # 无效签名
    invalid_signature = {'api_code': 1010, 'http_code': 400, 'api_msg': '无效签名'}
    # 无效数据格式
    invalid_format = {'api_code': 1011, 'http_code': 400, 'api_msg': '无效数据格式'}
    # 缺少方法名参数
    missing_method = {'api_code': 1012, 'http_code': 400, 'api_msg': '缺少方法名参数'}
    # 不存在的方法名
    invalid_method = {'api_code': 1013, 'http_code': 404, 'api_msg': '不存在的方法名'}
    # 缺少access_token参数
    missing_access_token = {'api_code': 1014, 'http_code': 400, 'api_msg': '缺少access_token参数'}
    # 无效access_token
    invalid_access_token = {'api_code': 1015, 'http_code': 401, 'api_msg': '无效access_token'}
    # api已经停用
    api_stop = {'api_code': 1016, 'http_code': 405, 'api_msg': 'api已经停用'}
    # 系统处理错误
    system_error = {'api_code': 1017, 'http_code': 500, 'api_msg': '系统处理错误'}
    # 缺少方法所需参数
    missing_arguments = {'api_code': 1018, 'http_code': 400, 'api_msg': '缺少方法所需参数'}
    # 不支持的http请求方式
    not_allowed_request = {'api_code': 1019, 'http_code': 405, 'api_msg': '不支持的http请求方式'}
    # 错误的API配置
    error_api_config = {'api_code': 1020, 'http_code': 500, 'api_msg': '错误的API配置'}
    # 无效的json格式
    invalid_json = {'api_code': 1021, 'http_code': 400, 'api_msg': '无效的json格式'}
    # 参数类型错误
    error_args_type = {'api_code': 1022, 'http_code': 400, 'api_msg': '参数类型错误'}


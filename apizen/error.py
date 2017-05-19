#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/19 上午8:54
# @Author  : Matrix
# @Site    : 
# @File    : error.py
# @Software: PyCharm

__author__ = 'blackmatrix'


class ApiBaseError(Exception):

    def __init__(self, err_code, message, status_code=500):
        self.err_code = err_code
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return str('异常编号：{code}; Http Code:{status_code}; 异常信息：{message}'.format(
            code=self.err_code,
            status_code=self.status_code,
            message=self.message))


# API 系统层面异常信息，以1000开始
class ApiSysError:
    # code 1000 为保留编码，代表执行成功
    # 服务不可用
    missing_system_error = ApiBaseError(err_code=1001, status_code=403, message='服务不可用')
    # 限制时间内调用失败次数
    app_call_limited = ApiBaseError(err_code=1002, status_code=403, message='限制时间内调用失败次数')
    # 请求被禁止
    forbidden_request = ApiBaseError(err_code=1003, status_code=403, message='请求被禁止')
    # 缺少版本参数
    missing_version = ApiBaseError(err_code=1004, status_code=400, message='缺少版本参数')
    # 不支持的版本号
    unsupported_version = ApiBaseError(err_code=1005, status_code=400, message='不支持的版本号')
    # 非法的版本参数
    invalid_version = ApiBaseError(err_code=1006, status_code=400, message='非法的版本参数')
    # 缺少时间戳参数
    missing_timestamp = ApiBaseError(err_code=1007, status_code=400, message='缺少时间戳参数')
    # 非法的时间戳参数
    invalid_timestamp = ApiBaseError(err_code=1008, status_code=400, message='非法的时间戳参数')
    # 缺少签名参数
    missing_signature = ApiBaseError(err_code=1009, status_code=400, message='缺少签名参数')
    # 无效签名
    invalid_signature = ApiBaseError(err_code=1010, status_code=400, message='无效签名')
    # 无效数据格式
    invalid_format = ApiBaseError(err_code=1011, status_code=400, message='无效数据格式')
    # 缺少方法名参数
    missing_method = ApiBaseError(err_code=1012, status_code=400, message='缺少方法名参数')
    # 不存在的方法名
    invalid_method = ApiBaseError(err_code=1013, status_code=404, message='不存在的方法名')
    # 缺少access_token参数
    missing_access_token = ApiBaseError(err_code=1014, status_code=400, message='缺少access_token参数')
    # 无效access_token
    invalid_access_token = ApiBaseError(err_code=1015, status_code=401, message='无效access_token')
    # api已经停用
    api_stop = ApiBaseError(err_code=1016, status_code=405, message='api已经停用')
    # 系统处理错误
    system_error = ApiBaseError(err_code=1017, status_code=500, message='系统处理错误')
    # 缺少方法所需参数
    missing_arguments = ApiBaseError(err_code=1018, status_code=400, message='缺少方法所需参数')
    # 不支持的http请求方式
    not_allowed_request = ApiBaseError(err_code=1019, status_code=405, message='不支持的http请求方式')
    # 错误的API配置
    error_api_config = ApiBaseError(err_code=1020, status_code=500, message='错误的API配置')
    # 无效的json格式
    invalid_json = ApiBaseError(err_code=1021, status_code=400, message='无效的json格式')
    # 参数类型错误
    error_args_type = ApiBaseError(err_code=1022, status_code=400, message='参数类型错误')


if __name__ == '__main__':
    pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/12 下午9:46
# @Author  : Matrix
# @Site    : 
# @File    : api_error.py
# @Software: PyCharm


# API接口异常
class ApiBaseError(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return str('异常编号：{code}; 异常信息：{message}'.format(code=self.code, message=self.message))


# API 系统层面异常信息，以1000开始
class ApiSysError:
    # code 1000 为保留编码，代表执行成功
    # 服务不可用
    missing_system_error = ApiBaseError(code=1001, message='服务不可用')
    # 限制时间内调用失败次数
    app_call_limited = ApiBaseError(code=1002, message='限制时间内调用失败次数')
    # 请求被禁止
    forbidden_request = ApiBaseError(code=1003, message='请求被禁止')
    # 缺少版本参数
    missing_version = ApiBaseError(code=1004, message='缺少版本参数')
    # 不支持的版本号
    unsupported_version = ApiBaseError(code=1005, message='不支持的版本号')
    # 非法的版本参数
    invalid_version = ApiBaseError(code=1006, message='非法的版本参数')
    # 缺少时间戳参数
    missing_timestamp = ApiBaseError(code=1007, message='缺少时间戳参数')
    # 非法的时间戳参数
    invalid_timestamp = ApiBaseError(code=1008, message='非法的时间戳参数')
    # 缺少签名参数
    missing_signature = ApiBaseError(code=1009, message='缺少签名参数')
    # 无效签名
    invalid_signature = ApiBaseError(code=1010, message='无效签名')
    # 无效数据格式
    invalid_format = ApiBaseError(code=1011, message='无效数据格式')
    # 缺少方法名参数
    missing_method = ApiBaseError(code=1012, message='缺少方法名参数')
    # 不存在的方法名
    invalid_method = ApiBaseError(code=1013, message='不存在的方法名')
    # 缺少access_token参数
    missing_access_token = ApiBaseError(code=1014, message='缺少access_token参数')
    # 无效access_token
    invalid_access_token = ApiBaseError(code=1015, message='无效access_token')
    # api已经停用
    api_stop = ApiBaseError(code=1016, message='api已经停用')
    # 系统处理错误
    system_error = ApiBaseError(code=1017, message='系统处理错误')
    # 缺少方法所需参数
    missing_arguments = ApiBaseError(code=1018, message='缺少方法所需参数')
    # 不支持的http请求方式
    unsupported_request = ApiBaseError(code=1019, message='不支持的http请求方式')
    # 错误的API配置
    error_api_config = ApiBaseError(code=1020, message='错误的API配置')
    # 无效的json格式
    invalid_json = ApiBaseError(code=1021, message='无效的json格式')
    # 不支持的参数类型
    unsupported_var_positional = ApiBaseError(code=1022, message='不支持VAR_POSITIONAL参数类型')


# API 子系统（业务）层级执行结果，以2000开始
class ApiSubError:
    # code 2000 为保留编码
    unknown_error = ApiBaseError(code=2001, message='未知异常')
    other_error = ApiBaseError(code=2002, message='其它异常')
    empty_result = ApiBaseError(code=2003,  message='查询结果为空')

if __name__ == '__main__':
    pass

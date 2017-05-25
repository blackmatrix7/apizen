#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/19 上午8:54
# @Author  : Matrix
# @Site    : 
# @File    : exception.py
# @Software: PyCharm
from json import JSONDecodeError

__author__ = 'blackmatrix'

'''
接口异常类型的管理与继承
'''

_no_value = object()


class ApiException(Exception):

    def __init__(self,  message, err_code='0000', status_code=500):
        self.err_code = err_code
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return str('异常编号：{code} 异常信息：{message}'.format(
            code=self.err_code,
            message=self.message))

    # 让类实例变成可调用对象，用于接收自定义异常信息，并抛出
    def __call__(self, message=_no_value, *, err_code=_no_value, status_code=_no_value):
        if message is not _no_value:
            self.message = message
        if err_code is not _no_value:
            self.err_code = err_code
        if status_code is not _no_value:
            self.status_code = status_code
        return self


class MetaApiExceptions(type):

    def __getattribute__(self, item):
        # 改变ApiException继承关系，支持将ApiException自定义为任何异常类型的子类
        ex_conf = super().__getattribute__(item)
        supers = (ex_conf.get('ex_type'), Exception) \
            if ex_conf.get('ex_type') and ex_conf.get('ex_type') is not Exception \
            else (Exception, )
        api_ex = type(item, (ApiException, *supers, ), {})
        return api_ex(**{'err_code': ex_conf['api_code'], 'message': ex_conf['api_msg'], 'status_code': ex_conf['http_code']})


class ApiBaseExceptions(metaclass=MetaApiExceptions):

    def __init__(self):
        pass


# API 系统层面异常信息，以1000开始
class ApiSysExceptions(ApiBaseExceptions):
    # code 1000 为保留编码，代表执行成功
    # 服务不可用
    missing_system_error = {'api_code': 1001, 'http_code': 403, 'api_msg': '服务不可用', 'ex_type': Exception}
    # 限制时间内调用失败次数
    app_call_limited = {'api_code': 1002, 'http_code': 403, 'api_msg': '限制时间内调用失败次数', 'ex_type': Exception}
    # 请求被禁止
    forbidden_request = {'api_code': 1003, 'http_code': 403, 'api_msg': '请求被禁止', 'ex_type': Exception}
    # 缺少版本参数
    missing_version = {'api_code': 1004, 'http_code': 400, 'api_msg': '缺少版本参数', 'ex_type': KeyError}
    # 不支持的版本号
    unsupported_version = {'api_code': 1005, 'http_code': 400, 'api_msg': '不支持的版本号', 'ex_type': ValueError}
    # 非法的版本参数
    version_stop = {'api_code': 1006, 'http_code': 400, 'api_msg': '接口版本已停用', 'ex_type': ValueError}
    # 缺少时间戳参数
    missing_timestamp = {'api_code': 1007, 'http_code': 400, 'api_msg': '缺少时间戳参数', 'ex_type': KeyError}
    # 非法的时间戳参数
    invalid_timestamp = {'api_code': 1008, 'http_code': 400, 'api_msg': '非法的时间戳参数', 'ex_type': ValueError}
    # 缺少签名参数
    missing_signature = {'api_code': 1009, 'http_code': 400, 'api_msg': '缺少签名参数', 'ex_type': KeyError}
    # 无效签名
    invalid_signature = {'api_code': 1010, 'http_code': 400, 'api_msg': '无效签名', 'ex_type': ValueError}
    # 无效数据格式
    invalid_format = {'api_code': 1011, 'http_code': 400, 'api_msg': '无效数据格式', 'ex_type': ValueError}
    # 缺少方法名参数
    missing_method = {'api_code': 1012, 'http_code': 400, 'api_msg': '缺少方法名参数', 'ex_type': KeyError}
    # 不存在的方法名
    invalid_method = {'api_code': 1013, 'http_code': 404, 'api_msg': '不存在的方法名', 'ex_type': AttributeError}
    # 缺少access_token参数
    missing_access_token = {'api_code': 1014, 'http_code': 400, 'api_msg': '缺少access_token参数', 'ex_type': KeyError}
    # 无效access_token
    invalid_access_token = {'api_code': 1015, 'http_code': 401, 'api_msg': '无效access_token', 'ex_type': ValueError}
    # api已经停用
    api_stop = {'api_code': 1016, 'http_code': 405, 'api_msg': 'api已经停用', 'ex_type': Exception}
    # 系统处理错误
    system_error = {'api_code': 1017, 'http_code': 500, 'api_msg': '系统处理错误', 'ex_type': Exception}
    # 缺少方法所需参数
    missing_arguments = {'api_code': 1018, 'http_code': 400, 'api_msg': '缺少方法所需参数', 'ex_type': KeyError}
    # 不支持的http请求方式
    not_allowed_request = {'api_code': 1019, 'http_code': 405, 'api_msg': '不支持的http请求方式', 'ex_type': Exception}
    # 错误的API配置
    error_api_config = {'api_code': 1020, 'http_code': 500, 'api_msg': '错误的API配置', 'ex_type': NotImplementedError}
    # 无效的json格式
    invalid_json = {'api_code': 1021, 'http_code': 400, 'api_msg': '无效的json格式', 'ex_type': JSONDecodeError}
    # 参数类型错误
    error_args_type = {'api_code': 1022, 'http_code': 400, 'api_msg': '参数类型错误', 'ex_type': KeyError}

if __name__ == '__main__':
    raise ApiSysExceptions.error_api_config('你好啊')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/7/26 21:44
# @Author  : BlackMatrix
# @Site : 
# @File : manager.py
# @Software: PyCharm
import importlib
from flask import Blueprint
from datetime import datetime
from collections import Iterable
from .method import get_method, run_method
from flask import g, request, jsonify, current_app
from .exceptions import SysException, ApiSysExceptions
from werkzeug.exceptions import BadRequest, BadRequestKeyError
from .config import (APIZEN_ROUTE,  APIZEN_VERSIONS, ACTIVATE_DEFAULT_ROUTE)

__author__ = 'blackmatrix'

"""
-------------------------------
ApiZen初始化管理模块
-------------------------------
适用版本：Flask
"""


# 创建蓝图
apizen = Blueprint('apizen', __name__)


class ApiZenManager:

    def __init__(self, app=None,
                 routes=None,
                 resp_fmt=None,
                 before_request=None,
                 after_request=None,
                 missing_args=None,
                 bad_request=None,
                 api_exception=None,
                 other_exception=None):
        self.app = app
        self.routes = routes
        self.resp_fmt = resp_fmt
        self.api_routing = default_api_routing
        self.before_request = before_request or default_before_request
        self.after_request = after_request or default_after_request
        self.missing_args = missing_args or default_missing_args
        self.bad_request = bad_request or default_bad_request
        self.api_exception = api_exception or default_api_exception
        self.other_exception = other_exception or default_other_exception
        if self.app is not None:
            self.init_app(app)

    def init_app(self, app,
                 routes=None,
                 before_request=None,
                 after_request=None,
                 missing_args=None,
                 bad_request=None,
                 api_exception=None,
                 other_exception=None):
        """
        初始化App，并且可以自定义一些handler
        :param app: Flask App
        :param routes: 自定义路由规则
        :param before_request: Flask 接口请求前触发的钩子函数
        :param after_request: Flask 接口请求后触发的钩子函数
        :param missing_args: Flask 接口请求参数缺失时触发的钩子函数
        :param bad_request: Flask 接口请求异常时触发的钩子函数
        :param api_exception: Flask 接口调用引发Api异常时触发的钩子函数
        :param other_exception: Flask 接口调用引发异常时触发的钩子函数（Api异常除外）
        :return:
        """
        self.app = app or self.app

        # 只有选择激活默认路由，才会注册对应的handler 与 blueprint
        if app.config.setdefault('ACTIVATE_DEFAULT_ROUTE', ACTIVATE_DEFAULT_ROUTE):
            self.routes = routes or self.routes or app.config.setdefault('APIZEN_ROUTE', APIZEN_ROUTE)
            self.before_request = before_request or self.before_request
            self.after_request = after_request or self.after_request
            self.missing_args = missing_args or self.missing_args
            self.bad_request = bad_request or self.bad_request
            self.api_exception = api_exception or self.api_exception
            self.other_exception = other_exception or self.other_exception
            # 在蓝图上注册handler
            self.register_handler()
            # 在蓝图上注册路由
            if isinstance(self.routes, Iterable) and not isinstance(self.routes, (str, bytes)):
                for route in self.routes:
                    apizen.route(route, methods=['GET', 'POST'])(self.api_routing)
            elif isinstance(self.routes, (str, bytes)):
                apizen.route(self.routes, methods=['GET', 'POST'])(self.api_routing)
            # 注册蓝图
            app.register_blueprint(apizen)

        # 导入Api版本
        self.import_api_versions(versions=app.config.setdefault('APIZEN_VERSIONS', APIZEN_VERSIONS))

    # 在蓝图上注册handler
    def register_handler(self):
        apizen.before_request(self.before_request)
        apizen.after_request(self.after_request)
        apizen.errorhandler(BadRequestKeyError)(self.missing_args)
        apizen.errorhandler(BadRequest)(self.bad_request)
        apizen.errorhandler(SysException)(self.api_exception)
        apizen.errorhandler(Exception)(self.other_exception)

    # 导入Api版本
    @staticmethod
    def import_api_versions(versions):
        if versions:
            for version in versions:
                importlib.import_module(version)


def format_retinfo(response=None, err_code=1000,
                   api_msg='执行成功', dev_msg=None):
    """
    格式化接口返回结果
    :param err_code:
    :param api_msg:
    :param dev_msg:
    :param response:
    :return:
    """
    return {
        'meta': {
                'code': err_code,
                'message': '{0}: {1}'.format(api_msg, dev_msg)
                if current_app.config['DEBUG'] and dev_msg else api_msg
            },
        'response': response
    }


# 对应的路由：@apizen.route(r'/api/router/rest', methods=['GET', 'POST'])
def default_api_routing():
    _method = request.args['method']
    _v = request.args['v']

    # 检查 content-type
    if request.method == 'POST':
        if request.content_type is None:
            raise ApiSysExceptions.missing_content_type
        if 'application/json' not in request.content_type \
                and 'application/x-www-form-urlencoded' not in request.content_type:
            raise ApiSysExceptions.unacceptable_content_type

    # 获取请求参数，参数优先级 json > form > querystring
    request_args = request.args.to_dict()
    if request.form:
        request_args.update(request.form.to_dict())
    if request.is_json and request.json:
        request_args.update(request.json)

    # 获取接口处理函数，及接口部分配置
    api_func, raw_resp, *_ = get_method(version=_v, api_method=_method, http_method=request.method)

    # 将请求参数传入接口处理函数并运行
    result = run_method(api_func, request_params=request_args)

    if raw_resp is False:
        result = format_retinfo(result)

    g.result = result
    g.status_code = 200
    resp = jsonify(result)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp, 200


# 对应的路由：@apizen.before_request
def default_before_request():
    request_param = {key.lower(): value for key, value in request.environ.items()
                     if key in ('CONTENT_TYPE', 'CONTENT_LENGTH', 'HTTP_HOST',
                                'HTTP_ACCEPT', 'HTTP_ACCEPT_ENCODING', 'HTTP_COOKIE',
                                'HTTP_USER_AGENT', 'PATH_INFO', 'QUERY_STRING',
                                'SERVER_PROTOCOL', 'REQUEST_METHOD', 'HTTP_HOST',
                                'SERVER_PORT', 'SERVER_SOFTWARE', 'REMOTE_ADDR',
                                'REMOTE_PORT', 'HTTP_ACCEPT_LANGUAGE')}
    g.request_raw_data = request.get_data().decode('utf8')
    g.request_time = datetime.now()
    g.api_method = request.args['method']
    g.api_version = request.args['v']
    g.request_param = request_param
    g.request_form = request.form.to_dict() if request.form else None
    try:
        g.request_json = request.get_json() if request.is_json else None
    except Exception:
        raise ApiSysExceptions.invalid_json


# 对应的路由：@apizen.default_after_request
def default_after_request(param):
    response_param = {'charset': param.charset,
                      'content_length': param.content_length,
                      'content_type': param.content_type,
                      'content_encoding': param.content_encoding,
                      'mimetype': param.mimetype,
                      'response': g.result if hasattr(g, 'result') else None,
                      'status': param.status,
                      'status_code': param.status_code}
    g.response_time = datetime.now()
    time_consuming = str(g.response_time - g.request_time)
    log_info = {'api_method': g.get('api_method'), 'api_version': g.get('api_version'),
                'request_param': g.get('request_param'), 'request_form': g.get('request_form'),
                'querystring': g.get('request_param')['query_string'], 'request_json': g.get('request_json'),
                'response_param': response_param, 'request_raw_data': g.request_raw_data,
                'request_time': g.get('request_time').strftime(current_app.config['APIZEN_DATETIME_FMT']),
                'response_time': g.get('response_time').strftime(current_app.config['APIZEN_DATETIME_FMT']),
                'time_consuming': time_consuming}
    if param.status_code >= 400:
        current_app.logger.error(log_info)
    else:
        current_app.logger.debug(log_info)
    return param


# 异常处理方法
def _exception_handler(ex, retinfo):
    g.result = retinfo
    g.status_code = ex.http_code
    if current_app.config['DEBUG'] and ex.http_code >= 500:
        raise ex
    else:
        resp = jsonify(retinfo)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, ex.http_code


# 对应的路由：@apizen.errorhandler(BadRequestKeyError)
def default_missing_args(ex):
    api_ex = ApiSysExceptions.missing_arguments
    retinfo = format_retinfo(err_code=api_ex.err_code,
                             api_msg=api_ex.err_msg,
                             dev_msg=','.join(ex.args))
    return _exception_handler(api_ex, retinfo)


# 对应的路由：@apizen.errorhandler(BadRequest)
def default_bad_request(ex):
    api_ex = ApiSysExceptions.bad_request
    retinfo = format_retinfo(err_code=api_ex.err_code,
                             api_msg=api_ex.err_msg,
                             dev_msg=ex.description)
    return _exception_handler(api_ex, retinfo)


# 对应的路由：@apizen.errorhandler(SysException)
def default_api_exception(api_ex):
    retinfo = format_retinfo(err_code=api_ex.err_code,
                             api_msg=api_ex.err_msg)
    return _exception_handler(api_ex, retinfo)


# 对应的路由：@apizen.errorhandler(Exception)
def default_other_exception(ex):
    api_ex = ApiSysExceptions.system_error
    retinfo = format_retinfo(err_code=api_ex.err_code,
                             api_msg=api_ex.err_msg,
                             dev_msg=ex)
    return _exception_handler(api_ex, retinfo)


if __name__ == '__main__':
    pass


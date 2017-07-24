#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/5/28 21:49
# @Author : BlackMatrix
# @Site :
# @File : routing.py
# @Software: PyCharm
from flask import Blueprint
from decimal import Decimal
from .method import Method
from datetime import datetime
from collections import Iterable
from flask.json import JSONEncoder
from flask import g, request, jsonify, current_app
from .exceptions import SysException, ApiSysExceptions
from werkzeug.exceptions import BadRequest, BadRequestKeyError

__author__ = 'blackmatrix'

# 创建蓝图
apizen = Blueprint('apizen', __name__)


class ApiZen:

    def __init__(self):
        self.before_request = None
        self.after_request = None
        self.missing_args = None
        self.bad_request = None
        self.api_exception = None
        self.other_exception = None

    def init_app(self, app, routes=None,
                 resp_fmt=None,
                 before_request=None,
                 after_request=None,
                 missing_args=None,
                 bad_request=None,
                 api_exception=None,
                 other_exception=None):
        """
        初始化App
        :param app: Flask App
        :param routes: 自定义路由规则
        :param resp_fmt: 自定义返回数据格式
        :param before_request: Flask 接口请求前触发的钩子函数
        :param after_request: Flask 接口请求后触发的钩子函数
        :param missing_args: Flask 接口请求参数缺失时触发的钩子函数
        :param bad_request: Flask 接口请求异常时触发的钩子函数
        :param api_exception: Flask 接口调用引发Api异常时触发的钩子函数
        :param other_exception: Flask 接口调用引发异常时处罚的钩子函数（Api异常除外）
        :return:
        """

        def get_handler(handler, default_hanlder):
            if handler is not None and callable(handler):
                return handler
            else:
                return default_hanlder

        self.before_request = get_handler(before_request, default_before_request)
        self.after_request = get_handler(after_request, default_after_request)
        self.missing_args = get_handler(missing_args, default_missing_args)
        self.bad_request = get_handler(bad_request, default_bad_request)
        self.api_exception = get_handler(api_exception, default_api_exception)
        self.other_exception = get_handler(other_exception, default_other_exception)

        # 在蓝图上注册handler
        self.register_handler()

        # 在蓝图上注册路由
        if routes is None:
            routes = app.config['APIZEN_ROUTE']
        if isinstance(routes, Iterable) and not isinstance(routes, (str, bytes)):
            for route in routes:
                apizen.route(route, methods=['GET', 'POST'])(api_routing)
        elif isinstance(routes, (str, bytes)):
            apizen.route(routes, methods=['GET', 'POST'])(api_routing)

        # 把蓝图注册到Flask App上
        app.register_blueprint(apizen)

        # 自定义日期格式，待修改
        datetime_format = app.config.get('APIZEN_DATETIME_FMT', '%Y/%m/%d %H:%M:%S')
        ApiZenJSONEncoder.datetime_format = datetime_format
        app.json_encoder = ApiZenJSONEncoder

    # 在蓝图上注册handler
    def register_handler(self):
        apizen.before_request(self.before_request)
        apizen.after_request(self.after_request)
        apizen.errorhandler(BadRequestKeyError)(self.missing_args)
        apizen.errorhandler(BadRequest)(self.bad_request)
        apizen.errorhandler(SysException)(self.api_exception)
        apizen.errorhandler(Exception)(self.other_exception)


class ApiZenJSONEncoder(JSONEncoder):

    datetime_format = None

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime(ApiZenJSONEncoder.datetime_format)
            elif isinstance(obj, Decimal):
                # 不转换为float是为了防止精度丢失
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


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
def api_routing(v=None, method=None):
    _method = method if method else request.args['method']
    _v = v if v else request.args['v']

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
    api_func, raw_resp, *_ = Method.get(version=_v, method_name=_method, request_method=request.method)

    # 将请求参数传入接口处理函数并运行
    result = Method.run(api_func, request_params=request_args)

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
        from app.tasks import send_mail_async
        send_mail_async.delay(current_app.config['ADMIN_EMAIL'], 'Web Api Request Error', 'api_error', **log_info)
        current_app.logger.error(log_info)
    else:
        current_app.logger.debug(log_info)
    return param


# 对应的路由：@apizen.errorhandler(BadRequestKeyError)
def default_missing_args(ex):
    api_ex = ApiSysExceptions.missing_arguments
    retinfo = format_retinfo(err_code=api_ex.err_code,
                             api_msg=api_ex.err_msg,
                             dev_msg=','.join(ex.args))
    if current_app.config['DEBUG'] and api_ex.http_code >= 500:
        raise ex
    else:
        resp = jsonify(retinfo)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, api_ex.http_code


# 对应的路由：@apizen.errorhandler(BadRequest)
def default_bad_request(ex):
    api_ex = ApiSysExceptions.bad_request
    retinfo = format_retinfo(err_code=api_ex.err_code,
                             api_msg=api_ex.err_msg,
                             dev_msg=ex.description)
    if current_app.config['DEBUG'] and api_ex.http_code >= 500:
        raise ex
    else:
        resp = jsonify(retinfo)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, api_ex.http_code


# 对应的路由：@apizen.errorhandler(SysException)
def default_api_exception(api_ex):
    retinfo = format_retinfo(err_code=api_ex.err_code,
                             api_msg=api_ex.err_msg)
    g.result = retinfo
    g.status_code = api_ex.http_code
    if current_app.config['DEBUG'] and api_ex.http_code >= 500:
        raise api_ex
    else:
        resp = jsonify(retinfo)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, api_ex.http_code


# 对应的路由：@apizen.errorhandler(Exception)
def default_other_exception(ex):
    api_ex = ApiSysExceptions.system_error
    retinfo = format_retinfo(err_code=api_ex.err_code,
                             api_msg=api_ex.err_msg,
                             dev_msg=ex)
    g.result = retinfo
    g.status_code = api_ex.http_code
    if current_app.config['DEBUG'] and api_ex.http_code >= 500:
        raise ex
    else:
        resp = jsonify(retinfo)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, api_ex.http_code

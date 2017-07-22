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
from flask.json import JSONEncoder
from flask import g, request, jsonify, current_app
from .exceptions import SysException, ApiSysExceptions
from werkzeug.exceptions import BadRequest, BadRequestKeyError

__author__ = 'blackmatrix'

# 创建蓝图
apizen = Blueprint('apizen', __name__)


class ApiZen:

    @staticmethod
    def init_app(app):
        apizen.before_request(before_request)
        apizen.after_request(after_request)
        apizen.before_request(before_request)
        apizen.errorhandler(BadRequestKeyError)(missing_arguments)
        apizen.errorhandler(BadRequest)(bad_request)
        apizen.errorhandler(SysException)(api_exception)
        apizen.errorhandler(Exception)(other_exception)
        apizen.route(app.config['APIZEN_ROUTE'], methods=['GET', 'POST'])(api_routing)
        app.register_blueprint(apizen)
        datetime_format = app.config.get('APIZEN_DATETIME_FORMAT', '%Y/%m/%d %H:%M:%S')
        ApiZenJSONEncoder.datetime_format = datetime_format
        app.json_encoder = ApiZenJSONEncoder


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


# @apizen.route(r'/api/router/rest', methods=['GET', 'POST'])
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


# @apizen.before_request
def before_request():
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


# @apizen.after_request
def after_request(param):
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
                'request_time': g.get('request_time').strftime(current_app.config['APIZEN_DATETIME_FORMAT']),
                'response_time': g.get('response_time').strftime(current_app.config['APIZEN_DATETIME_FORMAT']),
                'time_consuming': time_consuming}
    if param.status_code >= 400:
        from app.tasks import send_mail_async
        send_mail_async.delay(current_app.config['ADMIN_EMAIL'], 'Web Api Request Error', 'api_error', **log_info)
        current_app.logger.error(log_info)
    else:
        current_app.logger.debug(log_info)
    return param


# @apizen.errorhandler(BadRequestKeyError)
def missing_arguments(ex):
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


# @apizen.errorhandler(BadRequest)
def bad_request(ex):
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


# @apizen.errorhandler(SysException)
def api_exception(api_ex):
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


# @apizen.errorhandler(Exception)
def other_exception(ex):
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

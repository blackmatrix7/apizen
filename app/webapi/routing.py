#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/5/28 21:49
# @Author : BlackMatrix
# @Site :
# @File : routing.py
# @Software: PyCharm
from ..webapi import webapi
from datetime import datetime
from app.database import ModelBase
from app.apizen.methods import Method
from flask import g, request, jsonify, current_app
from werkzeug.exceptions import BadRequest, BadRequestKeyError
from app.apizen.exceptions import ApiException, ApiSysExceptions

__author__ = 'blackmatrix'


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
                'message': '{0}: {1}'.format(api_msg, dev_msg) if dev_msg else api_msg
            },
        'respone': response
    }


@webapi.route(r'/router/rest', methods=['GET', 'POST'])
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
    if request.json:
        request_args.update(request.json.to_dict())

    # 获取接口处理函数，及接口部分配置
    api_func, is_format, *_ = Method.get(version=_v, method_name=_method, request_method=request.method)

    # 将请求参数传入接口处理函数并运行
    result = Method.run(api_func, request_params=request_args)

    if isinstance(result, ModelBase) and hasattr(result, 'to_dict'):
        result = result.to_dict()
    if is_format:
        result = format_retinfo(result)

    g.result = result
    g.status_code = 200
    return jsonify(result), 200


@webapi.before_app_request
def before_app_request():
    request_param = {key.lower(): value for key, value in request.environ.items()
                     if key in ('CONTENT_TYPE', 'CONTENT_LENGTH', 'HTTP_HOST',
                                'HTTP_ACCEPT', 'HTTP_ACCEPT_ENCODING', 'HTTP_COOKIE',
                                'HTTP_USER_AGENT', 'PATH_INFO', 'QUERY_STRING',
                                'SERVER_PROTOCOL', 'REQUEST_METHOD', 'HTTP_HOST',
                                'SERVER_PORT', 'SERVER_SOFTWARE', 'REMOTE_ADDR',
                                'REMOTE_PORT', 'HTTP_ACCEPT_LANGUAGE')}
    g.request_time = datetime.now()
    g.api_method = request.args['method']
    g.api_version = request.args['v']
    g.request_environ = request_param
    g.request_form = request.form.to_dict() if request.form else None
    g.request_json = request.json.to_dict() if request.json else None


@webapi.after_app_request
def after_app_request(param):
    response_param = {'charset': param.charset,
                      'content_length': param.content_length,
                      'content_type': param.content_type,
                      'content_encoding': param.content_encoding,
                      'mimetype': param.mimetype,
                      'response': g.result if hasattr(g, 'result') else None,
                      'status': param.status,
                      'status_code': param.status_code}
    g.response_time = datetime.now()
    time_consuming = g.response_time - g.request_time
    if param.status_code >= 400 and not current_app.config['DEBUG']:
        from app.email import send_mail
        send_mail(current_app.config['ADMIN_EMAIL'], 'Web Api Request Error', 'api_error',
                  request_form=g.request_form, request_json=g.request_json,
                  request_environ=g.request_environ, response_environ=response_param,
                  api_method=g.api_method, api_version=g.api_version,
                  request_time=g.request_time.strftime(current_app.config['DATETIME_FORMAT']),
                  response_time=g.response_time.strftime(current_app.config['DATETIME_FORMAT']),
                  time_consuming=time_consuming)
    return param


@webapi.errorhandler(BadRequestKeyError)
def missing_arguments(ex):
    api_ex = ApiSysExceptions.missing_arguments
    retinfo = format_retinfo(err_code=api_ex.err_code,
                             api_msg=api_ex.message,
                             dev_msg=','.join(ex.args))
    return jsonify(retinfo), api_ex.status_code


@webapi.errorhandler(BadRequest)
def bad_request(ex):
    if 'Failed to decode JSON object' in ex.description:
        api_ex = ApiSysExceptions.invalid_json
        retinfo = format_retinfo(err_code=api_ex.err_code,
                                 api_msg=api_ex.message)
        return jsonify(retinfo), api_ex.status_code


@webapi.errorhandler(ApiException)
def api_exception(api_ex):
    retinfo = format_retinfo(err_code=api_ex.err_code,
                             api_msg=api_ex.message)
    g.result = retinfo
    g.status_code = api_ex.status_code
    return jsonify(retinfo), api_ex.status_code


@webapi.errorhandler(Exception)
def other_exception(ex):
    api_ex = ApiSysExceptions.system_error
    retinfo = format_retinfo(err_code=api_ex.err_code,
                             api_msg=api_ex.message,
                             dev_msg=ex)
    return jsonify(retinfo), api_ex.status_code

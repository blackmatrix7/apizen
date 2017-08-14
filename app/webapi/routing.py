#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/7/27 下午3:13
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : routing.py
# @Software: PyCharm
from datetime import datetime
from flask import g, request, current_app
from app.apizen.exceptions import ApiSysExceptions

__author__ = 'blackmatrix'


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
                'request_time': g.get('request_time').strftime(current_app.config['APIZEN_DATETIME_FMT']),
                'response_time': g.get('response_time').strftime(current_app.config['APIZEN_DATETIME_FMT']),
                'time_consuming': time_consuming}
    if param.status_code >= 400:
        from app.tasks import send_mail_async
        # send_mail_async.delay(current_app.config['ADMIN_EMAIL'], 'Web Api Request Error', 'api_error', **log_info)
        current_app.logger.error(log_info)
    else:
        current_app.logger.debug(log_info)
    return param

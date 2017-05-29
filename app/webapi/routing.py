#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 21:49
# @Author  : BlackMatrix
# @Site    : 
# @File    : routing.py
# @Software: PyCharm
from app.apizen.methods import Method
from flask import jsonify
from flask import request
from werkzeug.exceptions import BadRequest, BadRequestKeyError

from app.apizen.exceptions import ApiException, ApiSysExceptions
from ..webapi import webapi

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
    request_args = request.args.to_dict()
    if request.form:
        request_args.update(request.form.to_dict())
    if request.json:
        request_args.update(request.json.to_dict())
    result = Method.run(version=_v,
                        method_name=_method,
                        request_method=request.method,
                        request_params=request_args)
    return jsonify(format_retinfo(result))


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
    return jsonify(retinfo), api_ex.status_code


@webapi.errorhandler(Exception)
def other_exception(ex):
    api_ex = ApiSysExceptions.system_error
    retinfo = format_retinfo(err_code=api_ex.err_code,
                             api_msg=api_ex.message,
                             dev_msg=ex)
    return jsonify(retinfo), api_ex.status_code

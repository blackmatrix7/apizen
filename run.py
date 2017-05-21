#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/5 下午8:57
# @Author  : Matrix
# @Site    : 
# @File    : run.py
# @Software: PyCharm
import tornado.web
import apizen.version
import tornado.ioloop
import webapi.api_list
from webapi.api_route import WebApiRoute
from webapi.api_list import ApiMethodV10, ApiMethodV11

__author__ = 'matrix'


def runserver():

    application = tornado.web.Application([
        (r'/api/router/rest', WebApiRoute),
    ])

    # web webapi 版本注册
    apizen.version.register(ApiMethodV10, ApiMethodV11)

    application.listen(port=8010)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    runserver()

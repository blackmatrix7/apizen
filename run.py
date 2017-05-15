#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/5 下午8:57
# @Author  : Matrix
# @Site    : 
# @File    : run.py
# @Software: PyCharm
import tornado.web
import tornado.ioloop
from webapi.api_route import WebApiRoute

__author__ = 'matrix'


def runserver():
    application = tornado.web.Application([
        (r'/api/router/rest', WebApiRoute),
    ])

    application.listen(port=8010)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    runserver()

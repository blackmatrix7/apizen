#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/7/6 下午9:18
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: worker
# @Software: PyCharm
from app import create_app
from app.extensions import celery

__author__ = 'blackmatix'

flask_app = create_app()

if __name__ == '__main__':
    with flask_app.app_context():
        celery.start()


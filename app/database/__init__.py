#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/5/29 0:10
# @Author : BlackMatrix
# @Site : https://github.com/blackmatrix7
# @File : __init__.py
# @Software: PyCharm
from flask.ext.sqlalchemy import SQLAlchemy

__author__ = 'blackmatix'

db = SQLAlchemy()


class ModelBase:

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)


class ModelMixin:
    pass


if __name__ == '__main__':
    pass

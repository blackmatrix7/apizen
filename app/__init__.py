#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:47
# @Author  : Matrix
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Flask
from app.apizen.flaskext import apizen
from app.config import configs
from app.database import db
from app.oauth import oauth
from app.user import user
from app.webapi import webapi

__author__ = 'blackmatrix'


def create_app(app_config='default'):

    app = Flask(__name__)
    
    # 读取配置文件
    app.config.from_object(configs[app_config])
    # 蓝图注册
    register_blueprints(app)
    # 扩展注册
    register_extensions(app)

    @app.route('/', methods=['GET'])
    def index():
        return '<h1>请直接调用接口</h1>'

    return app


def register_blueprints(app):
    app.register_blueprint(webapi, url_prefix='/api')
    app.register_blueprint(oauth, url_prefix='/oauth')
    app.register_blueprint(user, url_prefix='/user')


def register_extensions(app):
    db.init_app(app)
    apizen.init_app(app)


if __name__ == '__main__':
    pass

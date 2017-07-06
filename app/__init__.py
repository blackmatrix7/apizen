#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:47
# @Author  : Matrix
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Flask
from app.user import user
from app.oauth import oauth
from app.database import db
from app.webapi import webapi
from app.config import configs
from flask_environments import Environments
from app.exts import mail, celery, apizen, migrate

__author__ = 'blackmatrix'


def create_app(app_config=None):

    app = Flask(__name__)

    # 读取配置文件
    if app_config is None:
        env = Environments(app, var_name='env', default_env='None')
        env.from_object('app.config')
    else:
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
    mail.init_app(app)
    apizen.init_app(app)
    migrate.init_app(app, db)
    celery.config_from_object(app.config)


if __name__ == '__main__':
    pass

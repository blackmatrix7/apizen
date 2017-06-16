#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:47
# @Author  : Matrix
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
import sys
from flask import Flask
from app.user import user
from app.oauth import oauth
from app.database import db
from app.config import configs
from app.webapi import webapi
from flask_script import Manager
from flask_migrate import Migrate
from app.apizen.flaskext import apizen
from flask_environments import Environments

__author__ = 'blackmatrix'

migrate = Migrate()


class CustomManager(Manager):

        def __call__(self, app=None, **kwargs):
            """
            自定义Manager为了去除Options will be ignored.的警告
            如果由flask-script的Manger创建app，和很多扩展结合使用
            都非常不方便。
            """
            if app is None:
                app = self.app
                if app is None:
                    raise Exception("There is no app here. This is unlikely to work.")

            if isinstance(app, Flask):
                return app

            app = app(**kwargs)
            self.app = app
            return app


def create_app(app_config=None):

    app = Flask(__name__)

    # 读取配置文件
    if app_config is None:
        if sys.argv and len(sys.argv) >= 1 \
                and '-config' in sys.argv[1][: sys.argv[1].index('=')]:
            app_config = sys.argv[1][sys.argv[1].index('=') + 1:]
            app.config.from_object(configs[app_config])
        else:
            env = Environments(app, var_name='config', default_env='None')
            env.from_object('app.config')

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
    migrate.init_app(app, db)


if __name__ == '__main__':
    pass

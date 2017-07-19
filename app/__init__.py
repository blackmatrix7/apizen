#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:47
# @Author  : Matrix
# @Site    : 
# @File    : __init__.py
# @Software: PyCharm
from flask import Flask
from app.exts import db
from app.user import user
from app.oauth import oauth
from app.config import configs
from flask_script import Manager
from flask_environments import Environments
from app.exts import mail, celery, migrate, manager, apizen

__author__ = 'blackmatrix'


class CustomManager(Manager):

    def __call__(self, app=None, **kwargs):
        """
        自定义Manager为了去除Options will be ignored.的警告
        如果由flask-script的Manager创建app，和很多扩展结合使用
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
    app.register_blueprint(oauth, url_prefix='/oauth')
    app.register_blueprint(user, url_prefix='/user')


def register_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    celery.init_app(app)
    apizen.init_app(app)
    manager.init_app(app)
    migrate.init_app(app, db)

if __name__ == '__main__':
    pass

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
from decimal import Decimal
from datetime import datetime
from app.config import configs
from flask_script import Manager
from flask.json import JSONEncoder
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


class CustomJSONEncoder(JSONEncoder):

    datetime_format = None

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime(CustomJSONEncoder.datetime_format)
            elif isinstance(obj, Decimal):
                # 不转换为float是为了防止精度丢失
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


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

    # 自定义日期格式，待修改
    datetime_format = app.config.get('APIZEN_DATETIME_FMT', '%Y/%m/%d %H:%M:%S')
    CustomJSONEncoder.datetime_format = datetime_format
    app.json_encoder = CustomJSONEncoder

    @app.route('/', methods=['GET'])
    def index():
        return '<h1>请直接调用接口</h1>'

    return app


def register_blueprints(app):
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

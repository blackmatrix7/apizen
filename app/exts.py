#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/7/6 20:49
# @Author  : BlackMatrix
# @Site : 
# @File : extensions.py
# @Software: PyCharm
from flask import Flask
from flask_mail import Mail
from flask_celery import Celery
from flask_script import Manager
from flask_migrate import Migrate
from app.apizen import ApiZenManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import MigrateCommand
from app.webapi.routing import before_request, after_request

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

    def init_app(self, app):
        self.app = app
        self.add_command('db', MigrateCommand)
        self.add_option('-e', '--env', dest='app_config', required=False)


class CustomCelery(Celery):

    def init_app(self, app):
        self.config_from_object(app.config)


# Flask-Script
manager = CustomManager()

# SQLAlchemy
db = SQLAlchemy()

# Flask-Migrate
migrate = Migrate()

# Flask-Mail
mail = Mail()

# Celery
celery = Celery()

# ApiZen
apizen = ApiZenManager(before_request=before_request,
                       after_request=after_request)


if __name__ == '__main__':
    pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:48
# @Author  : Matrix
# @Site    : 
# @File    : manage.py
# @Software: PyCharm
from app import create_app
from app.database import db
from flask_script import Manager
from app.models.oauth import OAuthClient
from flask_migrate import Migrate, MigrateCommand

__author__ = 'blackmatrix'

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='app_config', required=False)
manager.add_command('db', MigrateCommand)


@manager.command
def devserver():
    # 必须在manager.run()之后才能获取到创建的Flask实例
    app = manager.app
    # migrate = Migrate(app, db)
    app.run()


@manager.command
def createdb():
    db.create_all()


@manager.command
def dropdb():
    db.drop_all()

if __name__ == '__main__':
    manager.run()


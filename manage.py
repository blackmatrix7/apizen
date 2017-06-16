#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:48
# @Author  : Matrix
# @Site    : 
# @File    : manage.py
# @Software: PyCharm
import app.database.models
from app.database import db
from app.user.controller import new_user
from flask_migrate import MigrateCommand
from app import create_app, CustomManager

__author__ = 'blackmatrix'


flask_app = create_app()
manager = CustomManager(flask_app)
manager.add_command('db', MigrateCommand)
manager.add_option('-c', '--config', dest='app_config', required=False)


@manager.command
def runserver():
    flask_app.run(host=flask_app.config['HOST'],  port=flask_app.config['PORT'])


@manager.command
def initadmin(email, user_name, password):
    new_user(email, user_name, password)


@manager.command
def createdb():
    db.create_all()


@manager.command
def dropdb():
    db.drop_all()

if __name__ == '__main__':
    manager.run()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:48
# @Author  : Matrix
# @Site    : 
# @File    : manage.py
# @Software: PyCharm
import sys
from celery import Celery
import app.database.models
from app.database import db
from app.user.controller import new_user
from flask_migrate import MigrateCommand
from app import create_app, CustomManager

__author__ = 'blackmatrix'

# command line env
if sys.argv and len(sys.argv) >= 1 and '-env' in sys.argv[1]:
    app_config = sys.argv[1][sys.argv[1].find('=') + 1:]
else:
    app_config = None

flask_app = create_app(app_config)

# Celery
import os
flask_celery = Celery(flask_app.name, broker=flask_app.config['CELERY_BROKER_URL'])
flask_celery.conf.update(flask_app.config)

# Flask-Script
manager = CustomManager(flask_app)
manager.add_command('db', MigrateCommand)
manager.add_option('-e', '--env', dest='app_config', required=False)


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


@manager.command
def celeryworks():
    flask_celery.start()

if __name__ == '__main__':
    manager.run()

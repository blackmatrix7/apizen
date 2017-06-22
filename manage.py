#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:48
# @Author  : Matrix
# @Site    : 
# @File    : manage.py
# @Software: PyCharm
import os
import sys
import logging.config
from celery import Celery
import app.database.models
from app.database import db
from app.user.controller import new_user
from flask_migrate import MigrateCommand
from app import create_app, CustomManager
from logging.handlers import TimedRotatingFileHandler

__author__ = 'blackmatrix'

# command line env
if sys.argv and len(sys.argv) >= 1 and '-env' in sys.argv[1]:
    app_config = sys.argv[1][sys.argv[1].find('=') + 1:]
else:
    app_config = None

flask_app = create_app(app_config)

# Flask-Logger
if not os.path.exists('logs'):
    os.mkdir('logs')
# 默认级别为ERROR，设置为DEBUG，记录INFO和DEBUG级别的日志
logging.basicConfig(level=logging.DEBUG)
fh = TimedRotatingFileHandler('logs/manage.log', 'midnight', 1, 10)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)s]')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
flask_app.logger.addHandler(fh)
flask_app.logger.addHandler(ch)

# Flask-Script
manager = CustomManager(flask_app)
manager.add_command('db', MigrateCommand)
manager.add_option('-e', '--env', dest='app_config', required=False)

# Celery
flask_celery = Celery(flask_app.name, broker=os.environ.get('CELERY_BROKER_URL'))
flask_celery.conf.update(flask_app.config)


@manager.command
def devserver():
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
def celery():
    cmd = 'env={config} celery -A manage.flask_celery worker --loglevel=info'.format(config=app_config)
    os.system(cmd)


@manager.command
def runserver():
    cmd = 'env={config} gunicorn -k gevent -w {workers} -b {host}:{port} manage:flask_app'.format(
        config=app_config,
        workers=flask_app.config['WORKS'],
        host=flask_app.config['HOST'],
        port=flask_app.config['PORT'])
    os.system(cmd)


if __name__ == '__main__':
    manager.run()

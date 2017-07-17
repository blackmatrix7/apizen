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
import app.database.models
from app import create_app
from app.database import db
from app.exts import manager
from app.user.controller import new_user
from logging.handlers import TimedRotatingFileHandler

__author__ = 'blackmatrix'

# command line env
if sys.argv and len(sys.argv) > 1 and '-env' in sys.argv[1]:
    app_config = sys.argv[1][sys.argv[1].find('=') + 1:]
else:
    app_config = None

flask_app = create_app(app_config)

# Flask-Logger
if not os.path.exists('logs'):
    os.mkdir('logs')
# 默认级别为ERROR，设置为DEBUG，记录INFO和DEBUG级别的日志
logging.basicConfig(level=logging.DEBUG)
logfile = os.path.abspath('logs/manage.log')
# 每个日志512k,保留10个日志文件
fh = TimedRotatingFileHandler('logs/manage.log', 'midnight', 1, 10)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)s]')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
flask_app.logger.addHandler(fh)
flask_app.logger.addHandler(ch)


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


# @manager.command
# def celery():
    # from app.extensions import celery as celery_app
    # with flask_app.app_context():
    #     celery_app.start('-A runcelery.celery worker --loglevel=info')
    # cmd = 'env={config} celery -A manage.flask_celery worker --loglevel=info'.format(config=app_config)
    # os.system(cmd)
#
#
# @manager.command
# def runserver():
#     cmd = 'env={config} gunicorn -k gevent -w {workers} -b {host}:{port} manage:flask_app'.format(
#         config=app_config,
#         workers=flask_app.config['WORKS'],
#         host=flask_app.config['HOST'],
#         port=flask_app.config['PORT'])
#     os.system(cmd)


if __name__ == '__main__':
    manager.run()

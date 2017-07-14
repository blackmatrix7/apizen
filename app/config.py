#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:50
# @Author  : BlackMatrix
# @Site    : 
# @File    : config.py
# @Software: PyCharm
import os

__author__ = 'blackmatrix'


class BaseConfig:

    DEBUG = True
    TESTING = False

    HOST = '0.0.0.0'
    PORT = 8080
    WORKS = 5

    SITE_NAME = 'ApiZen'
    LOGGER_NAME = 'Api Zen'

    # 数据配置
    MARIADB_HOST = os.environ.get('MARIADB_HOST', '127.0.0.1')
    MARIADB_PORT = os.environ.get('MARIADB_PORT', 3306)
    MARIADB_USER = os.environ.get('MARIADB_USER', 'apizen')
    MARIADB_PASS = os.environ.get('MARIADB_PASS', 'apizen')
    MARIADB_DB = os.environ.get('MARIADB_DB', 'apizen')

    # SQLAlchemy
    SQLALCHEMY_BINDS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(
        MARIADB_USER,
        MARIADB_PASS,
        MARIADB_HOST,
        MARIADB_PORT,
        MARIADB_DB
    )

    # API ZEN
    DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'

    # Celery
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_REDIRECT_STDOUTS_LEVEL = 'INFO'
    CELERY_IMPORTS = ('app.tasks', )
    # celery worker的并发数
    CELERYD_CONCURRENCY = 3
    # 默认队列
    CELERY_DEFAULT_QUEUE = 'celery@apizen.default'

    # Flask Mail
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', '').split(',')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
    SUBJECT_PREFIX = '[ApiZen]'


class DevConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    # 端口号
    PORT = 8080

    # 数据库配置
    MARIADB_HOST = os.environ.get('MARIADB_HOST', '127.0.0.1')
    MARIADB_PORT = os.environ.get('MARIADB_PORT', 3306)
    MARIADB_USER = os.environ.get('MARIADB_USER', 'apizen')
    MARIADB_PASS = os.environ.get('MARIADB_PASS', 'apizen')
    MARIADB_DB = os.environ.get('MARIADB_DB', 'apizen')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(
        MARIADB_USER,
        MARIADB_PASS,
        MARIADB_HOST,
        MARIADB_PORT,
        MARIADB_DB
    )

    # Celery
    # 默认队列
    CELERY_DEFAULT_QUEUE = 'celery@apizen.dev'


class TestConfig(BaseConfig):
    DEBUG = False
    TESTING = True

    # 端口号
    PORT = 8080

    # 数据库配置
    MARIADB_HOST = os.environ.get('MARIADB_HOST', '127.0.0.1')
    MARIADB_PORT = os.environ.get('MARIADB_PORT', 3306)
    MARIADB_USER = os.environ.get('MARIADB_USER', 'apizen')
    MARIADB_PASS = os.environ.get('MARIADB_PASS', 'apizen')
    MARIADB_DB = os.environ.get('MARIADB_DB', 'apizen')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(
        MARIADB_USER,
        MARIADB_PASS,
        MARIADB_HOST,
        MARIADB_PORT,
        MARIADB_DB
    )

    # Celery
    # 默认队列
    CELERY_DEFAULT_QUEUE = 'celery@apizen.test'


class ProdConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    # 端口号
    PORT = 8080
    WORKS = 5
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery
    # 默认队列
    CELERY_DEFAULT_QUEUE = 'celery@apizen.prod'


devcfg = DevConfig
testcfg = TestConfig
prodcfg = ProdConfig
default = DevConfig

configs = {
    'devcfg': devcfg,
    'testcfg': testcfg,
    'prodcfg': prodcfg,
    'default': default
}


if __name__ == '__main__':
    pass

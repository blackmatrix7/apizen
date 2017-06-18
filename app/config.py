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

    SITE_NAME = 'Api Zen'

    # DataBase Config
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
    CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
    CELERY_REDIRECT_STDOUTS_LEVEL = 'INFO'

    # Flask Mail
    ADMIN_EMAIL = ['huangxupeng@vcansenior.cn']
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
    SUBJECT_PREFIX = '[ApiZen]'


class DevConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    PORT = 8080


class TestConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(BaseConfig):
    PORT = 8080
    WORKS = 5

    SITE_NAME = 'Api Zen'
    DEBUG = False
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False


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

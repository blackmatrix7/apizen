#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:50
# @Author  : BlackMatrix
# @Site    : 
# @File    : config.py
# @Software: PyCharm
import os
__author__ = 'blackmatix'


class BaseConfig:

    DEBUG = True
    TESTING = False

    SITE_NAME = 'Api Zen'

    HOST = '0.0.0.0'
    PORT = 8080

    SQLALCHEMY_BINDS = {

    }

    MARIADB_HOST = os.environ.get('MARIADB_HOST', '127.0.0.1')
    MARIADB_PORT = os.environ.get('MARIADB_PORT', 1433)
    MARIADB_USER = os.environ.get('MARIADB_USER', 'apizen')
    MARIADB_PASS = os.environ.get('MARIADB_PASS', 'apizen')
    MARIADB_DB = os.environ.get('MARIADB_DB', 'apizen')

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(
        MARIADB_HOST,
        MARIADB_PASS,
        MARIADB_HOST,
        MARIADB_PORT,
        MARIADB_DB
    )


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class ProdConfig(BaseConfig):
    DEBUG = False

config = {
    'dev_config': DevConfig,
    'test_config': TestConfig,
    'prod_config': ProdConfig,
    'default': DevConfig
}


if __name__ == '__main__':
    pass

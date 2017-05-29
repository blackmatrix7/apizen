#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:48
# @Author  : Matrix
# @Site    : 
# @File    : manage.py
# @Software: PyCharm
from app import create_app
from app.database import db
from app.config import configs
from flask_script import Manager

__author__ = 'blackmatrix'


# 创建app
app = create_app()
manager = Manager(app)


@manager.command
def devserver(config='default'):
    app.init(app_config=config)
    app.run()


@manager.command
def createdb(config='default'):
    app.init(app_config=config)
    db.create_all()

if __name__ == '__main__':
    manager.run()


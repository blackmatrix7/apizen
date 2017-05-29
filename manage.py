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
from flask.ext.script import Manager

__author__ = 'blackmatrix'


def _make_context():
    return dict(
        app=create_app(configs.dev_config),
        db=db
    )

# 创建app
app = create_app()
manager = Manager(app)


@manager.command
def devserver(config='default'):
    app.config.from_object(configs[config])
    app.run()


@manager.command
def gunicron():
    pass


@manager.command
def createdb():
    db.create_all()

if __name__ == '__main__':
    manager.run()


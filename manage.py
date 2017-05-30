#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:48
# @Author  : Matrix
# @Site    : 
# @File    : manage.py
# @Software: PyCharm
import os
from app import create_app
from app.database import db
from flask_script import Manager
from app.models.oauth import OAuthClient
from flask_migrate import Migrate, MigrateCommand

__author__ = 'blackmatrix'


cfg_name = os.environ.get('APIZEN_CFG', 'default')
app = create_app(cfg_name)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def devserver():
    app.run()


@manager.command
def createdb():
    db.create_all()


@manager.command
def dropdb():
    db.drop_all()

if __name__ == '__main__':
    manager.run()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:48
# @Author  : Matrix
# @Site    : 
# @File    : manage.py
# @Software: PyCharm
from app import create_app
from app.database import db
from flask_script import Manager, Command, Option
from app.database.models import *
from app.user.controller import new_user
from flask_migrate import MigrateCommand

__author__ = 'blackmatrix'


class GunicornServer(Command):
    """Run the app within Gunicorn"""

    def get_options(self):
        from gunicorn.config import make_settings

        settings = make_settings()
        options = (
            Option(*klass.cli, action=klass.action)
            for setting, klass in settings.iteritems() if klass.cli
        )
        return options

    def run(self, *args, **kwargs):
        from gunicorn.app.wsgiapp import WSGIApplication

        app = WSGIApplication()
        app.app_uri = 'manage:app'
        return app.run()

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)
manager.add_option('-c', '--config', dest='app_config', required=False)
manager.add_command("gunicorn", GunicornServer())


@manager.command
def runserver():
    app = manager.app
    app.run(host=app.config['HOST'],  port=app.config['PORT'])


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

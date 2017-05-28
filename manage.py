#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:48
# @Author  : Matrix
# @Site    : 
# @File    : manage.py
# @Software: PyCharm
import sys
from app import create_app
from app.database import db
from app.config import config

__author__ = 'blackmatrix'


def _make_context():
    return dict(
        app=create_app(config.dev_config),
        db=db
    )

# 获取启动参数
config_name = sys.argv[1] if len(sys.argv) >= 2 else 'default'
action_name = sys.argv[2] if len(sys.argv) >= 3 else 'runserver'
# 读取配置文件
app_config = config[config_name]
# 创建app
app = create_app(app_config=app_config)


def run_server():
    app.run(port=app_config.PORT)


def create_db():
    db.create_all()

if __name__ == '__main__':
    action = {
        'run_server': run_server,
        'create_db': create_db
    }
    action[action_name]()


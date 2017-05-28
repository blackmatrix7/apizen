#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 20:48
# @Author  : Matrix
# @Site    : 
# @File    : manage.py
# @Software: PyCharm
import sys
from app import create_app
from app.config import config

__author__ = 'blackmatrix'

# 获取配置文件名称
config_name = sys.argv[1] if len(sys.argv) >= 2 else 'default'
action_name = sys.argv[2] if len(sys.argv) >= 3 else 'runserver'
# 读取配置文件
app_config = config[config_name]
# 创建app
app = create_app(app_config=app_config)


if __name__ == '__main__':
    if action_name == 'runserver':
        app.run(port=app_config.PORT)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/7/6 20:49
# @Author  : BlackMatrix
# @Site : 
# @File : extensions.py
# @Software: PyCharm
from flask_mail import Mail
from celery import Celery

__author__ = 'blackmatrix'

# Flask-Mail
mail = Mail()

# Celery
celery = Celery()


if __name__ == '__main__':
    pass

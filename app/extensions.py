#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/7/6 20:49
# @Author  : BlackMatrix
# @Site : 
# @File : extensions.py
# @Software: PyCharm
from celery import Celery
from flask_mail import Mail
from app.apizen.flaskext import ApiZen

__author__ = 'blackmatrix'

# ApiZen
apizen = ApiZen()

# Flask-Mail
mail = Mail()

# Celery
celery = Celery()


if __name__ == '__main__':
    pass

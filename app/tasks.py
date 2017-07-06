#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/6/18 12:53
# @Author  : BlackMatrix
# @Site : 
# @File : tasks.py
# @Software: PyCharm
from app.email import send_mail
from app.extensions import celery

__author__ = 'blackmatrix'


@celery.task
def send_mail_async(mail_to, subject, template, **kwargs):
    send_mail(mail_to, subject, template, **kwargs)


if __name__ == '__main__':
    pass

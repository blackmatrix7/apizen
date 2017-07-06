#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/6/18 上午12:54
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: __init__.py.py
# @Software: PyCharm
from manage import flask_app
from flask_mail import Message
from app.extensions import mail
from flask import render_template, current_app

__author__ = 'blackmatix'


def send_mail(mail_to, subject, template, **kwargs):
    # TODO 判断mail_to 必须是List
    with flask_app.app_context():
        _subject = '{0} {1}'.format(current_app.config['SUBJECT_PREFIX'], subject)
        _sender = current_app.config['MAIL_DEFAULT_SENDER']
        msg = Message(subject=_subject, sender=_sender, recipients=mail_to)
        msg.body = render_template('/email/{0}.txt'.format(template), **kwargs)
        mail.send(msg)

if __name__ == '__main__':
    pass

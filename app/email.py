#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/7/6 下午10:58
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: email.py
# @Software: PyCharm
from app.exts import mail
from manage import flask_app
from flask_mail import Message
from flask import render_template, current_app

__author__ = 'blackmatix'


def send_mail(mail_to, subject, template, **kwargs):
    # 在函数内部导入flask_app，避免交叉引用
    # TODO 判断mail_to 必须是List
    with flask_app.app_context():
        _subject = '{0} {1}'.format(current_app.config['SUBJECT_PREFIX'], subject)
        _sender = current_app.config['MAIL_DEFAULT_SENDER']
        msg = Message(subject=_subject, sender=_sender, recipients=mail_to)
        msg.body = render_template('/email/{0}.txt'.format(template), **kwargs)
        mail.send(msg)

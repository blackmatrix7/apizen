#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/6/7 下午9:25
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: controller.py
# @Software: PyCharm
from app.exts import db
from .models import User
from datetime import datetime
from ..webapi.exceptions import ApiSubExceptions

__author__ = 'blackmatix'


def user_login(email, password):
    user = db.session.query(User).filter(User.email == email,
                                         User.is_enable == 1).first()
    if user:
        if not user.verify_password(password):
            raise ApiSubExceptions.wrong_password
        user.last_login = datetime.now()
        user.upsert().commit()
        # TODO 登录成功后的处理
        return user
    else:
        raise ApiSubExceptions.wrong_password


def new_user(email, user_name, password):
    if User.get_by_email(email):
        raise ApiSubExceptions.email_registered
    user = User(email=email, user_name=user_name)
    user.password = password
    user.upsert().commit()
    # TODO 发送确认邮件
    return user


if __name__ == '__main__':
    pass

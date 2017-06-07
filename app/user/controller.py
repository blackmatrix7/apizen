#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/6/7 下午9:25
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: controller.py
# @Software: PyCharm
from .models import User
from ..database import db
from ..webapi.exceptions import ApiSubExceptions

__author__ = 'blackmatix'


def user_login(email, password):
    user = db.session.query(User).filter(User.email == email).first()
    if user:
        if not user.verify_password(password):
            raise ApiSubExceptions.wrong_password
        # TODO 登录成功后的处理
    else:
        raise ApiSubExceptions.wrong_password


if __name__ == '__main__':
    pass

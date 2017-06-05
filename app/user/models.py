#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/5/29 2:22
# @Author : BlackMatrix
# @Site : https://github.com/blackmatrix7
# @File : models.py
# @Software: PyCharm

from app.database import ModelBase, ModelMixin, db


class User(ModelBase, ModelMixin):

    __tablename__ = 'user'

    user_name = db.Column(db.String(40))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))


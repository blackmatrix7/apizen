#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/5/29 2:22
# @Author : BlackMatrix
# @Site : https://github.com/blackmatrix7
# @File : models.py
# @Software: PyCharm
from werkzeug.security import check_password_hash, generate_password_hash
from app.database import ModelBase, ModelMixin, db
from ..oauth.models import Client


class User(ModelBase, ModelMixin):

    __tablename__ = 'user'

    user_name = db.Column(db.String(40))
    password_hash = db.Column(db.String(200))
    email = db.Column(db.String(100))
    clients = db.relationship(Client, backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(password=value)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)




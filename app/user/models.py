#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/5/29 2:22
# @Author : BlackMatrix
# @Site : https://github.com/blackmatrix7
# @File : models.py
# @Software: PyCharm
import copy
from app.exts import db
from ..oauth.models import Client
from app.database import ModelBase
from werkzeug.security import check_password_hash, generate_password_hash


class User(ModelBase):

    __tablename__ = 'user'

    email = db.Column(db.String(100), nullable=False, index=True)
    user_name = db.Column(db.String(40), nullable=True, index=True)
    password_hash = db.Column(db.String(200))
    last_login = db.Column(db.DateTime)
    is_enable = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, nullable=True)

    @classmethod
    def get_by_email(cls, email):
        return db.session.query(cls).filter(cls.email == email).first()

    # 去除 password_hash 的显示
    def to_dict(self, columns=None):
        """
        将SQLALCHEMY MODEL 转换成 dict
        :param columns: dict 的 key, 如果为None, 则返回全部列
        :return:
        """
        if columns is None:
            columns = list(self.columns)
        _columns = copy.copy(columns)
        _columns.remove('password_hash')
        return super().to_dict(columns=_columns)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(password=value)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)




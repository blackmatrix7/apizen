#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/5/29 2:22
# @Author : BlackMatrix
# @Site : https://github.com/blackmatrix7
# @File : oauth
# @Software: PyCharm
from app.models import *
from app.database import ModelBase, ModelMixin, db

__author__ = 'blackmatix'


class OAuthClient(ModelBase, ModelMixin):

    __tablename__ = 'oauth_client'

    client_id = db.Column(db.Integer, nullable=False)
    client_name = db.Column(db.String(40), nullable=False)
    client_secret = db.Column(db.String(40), nullable=False)


if __name__ == '__main__':
    pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/5/29 2:22
# @Author : BlackMatrix
# @Site : https://github.com/blackmatrix7
# @File : oauth
# @Software: PyCharm
from app.database import ModelBase, ModelMixin, db

__author__ = 'blackmatix'


class Client(ModelBase, ModelMixin):
    name = db.Column(db.String(40))
    description = db.Column(db.String(400))
    user_id = db.Column(db.ForeignKey('User.id'))
    user = db.relationship('User')
    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), unique=True, index=True,
                              nullable=False)
    is_confidential = db.Column(db.Boolean)

    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


if __name__ == '__main__':
    pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/5/29 0:10
# @Author : BlackMatrix
# @Site : https://github.com/blackmatrix7
# @File : __init__.py
# @Software: PyCharm
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

__author__ = 'blackmatrix'

db = SQLAlchemy()


class ModelBase(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, index=True)
    created_time = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now,
                             onupdate=datetime.now)

    def __init__(self, **kwargs):
        columns = [c.name for c in self.__table__.columns]
        super().__init__(**{attr: value for attr, value in kwargs.items()
                            if attr in columns})


class ModelMixin(db.Model):

    __abstract__ = True

    def upsert(self, commit=False):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=False):
        db.session.delete(self)
        return commit and db.session.commit()

    def upsert_and_commit(self):
        self.upsert(commit=True)

    def delete_and_commit(self):
        self.delete(commit=True)

    def to_dict(self, columns=None):
        if columns is None:
            columns = (c.name for c in self.__table__.columns)
        return {c: getattr(self, c) for c in columns}

    def to_json(self):
        pass


if __name__ == '__main__':
    pass

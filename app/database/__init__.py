#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/5/29 0:10
# @Author : BlackMatrix
# @Site : https://github.com/blackmatrix7
# @File : __init__.py
# @Software: PyCharm
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

__author__ = 'blackmatix'

db = SQLAlchemy()


class ModelBase(db.Model):

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, index=True)
    created_time = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now,
                             onupdate=datetime.now)

    def __init__(self, **kwargs):
        columns = [c.name for c in self.__table__.columns]
        temp = {attr: value for attr, value in kwargs.items()
                            if attr in columns}
        super().__init__(**{attr: value for attr, value in kwargs.items()
                            if attr in columns})


class ModelMixin:

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


if __name__ == '__main__':
    pass

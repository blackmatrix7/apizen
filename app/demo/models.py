#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/6/20 21:06
# @Author  : BlackMatrix
# @Site : 
# @File : models.py
# @Software: PyCharm
from app.database import ModelBase, ModelMixin, db
__author__ = 'blackmatrix'


class DemoParent(ModelBase, ModelMixin):

    __tablename__ = 'demo_parent'

    name = db.Column(db.String(40))
    children = db.relationship('DemoChild', backref='demo_parent')


class DemoChild(ModelBase, ModelMixin):

    __tablename__ = 'demo_child'

    parent_id = db.Column(db.ForeignKey(DemoParent.id))
    name = db.Column(db.String(40))

if __name__ == '__main__':
    pass

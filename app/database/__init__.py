#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/5/29 0:10
# @Author : BlackMatrix
# @Site : https://github.com/blackmatrix7
# @File : __init__.py
# @Software: PyCharm
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect

__author__ = 'blackmatrix'

db = SQLAlchemy()


class ModelMixin:

    __abstract__ = True

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def upsert(self):
        db.session.add(self)
        return self

    def delete(self):
        db.session.delete(self)
        return self

    @property
    def columns(self):
        yield from (c.name for c in self.__table__.columns)

    @staticmethod
    def commit():
        db.session.commit()

    @classmethod
    def get_by_id(cls, id_):
        return db.session.query(cls).filter(cls.id == int(id_)).first()

    @classmethod
    def from_dict(cls, **kwargs):
        """
        临时方案,通过参数快速创建model,支持过滤掉多余的参数。
        :param kwargs:
        :return:
        """
        columns = [c.name for c in cls.__table__.columns]
        relationships = inspect(cls).relationships
        super().__init__(**{attr: value for attr, value in kwargs.items() if attr in (columns, relationships)})

    def to_dict(self, columns=None):
        """
        将SQLALCHEMY MODEL 转换成 dict
        :param columns: dict 的 key, 如果为None, 则返回全部列
        :return:
        """
        if columns is None:
            columns = self.columns
        return {c: getattr(self, c) for c in columns}


class ModelBase(ModelMixin, db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, index=True)
    created_time = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now,
                             onupdate=datetime.now)

    def __init__(self, **kwargs):
        columns = [c.name for c in self.__table__.columns]
        relationships = inspect(self.__class__).relationships
        for attr, value in relationships.items():
            loc = locals()
            print(attr, value)

        # relationships = [key for key, value in inspect(self.__class__).relationships.items()]
        # args = {attr: value for attr, value in kwargs.items() if (attr in columns)}
        # args.update({attr: value for attr, value in kwargs.items() if (attr in relationships)})
        # super().__init__(**args)
        # loc = locals()
        # for attr, value in relationships.items():
        #     print(attr, value)
        # table_kw = {attr: attr(**value) for attr, value in relationships.items() if attr in kwargs}
        # super().__init__(**{attr: value for attr, value in kwargs.items()
        #                     if attr in columns})

    # def __init__(self, *args, **kwargs):
    #     model(**{key: value
    #                 for key, value in data.items()
    #                 if key in model.__table__.columns})
    #     table = self.__table__
    #     columns = table.columns
    #     temp = table.__dict__
    #     from sqlalchemy.inspection import inspect
    #     table_relationships = inspect(self.__class__).relationships
    #     print(columns)


if __name__ == '__main__':
    pass

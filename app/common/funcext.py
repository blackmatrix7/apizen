#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/6/7 下午11:52
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: funcext.py
# @Software: PyCharm
from datetime import datetime
from flask.json import JSONEncoder

__author__ = 'blackmatix'


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%Y/%m/%d %H:%M:%S')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


if __name__ == '__main__':
    pass

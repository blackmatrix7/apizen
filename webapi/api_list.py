# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/3/14 8:43
# @Author: Matrix
# @Site:
# @File: api_list.py
# @Software: PyCharm
from services.demo.api_demo import ApiDemo

__author__ = 'matrix'

api_demo = ApiDemo()

api = {
    '1.0':
        {
            'matrix.api.demo.demo1': {'func': api_demo.demo1},
            'matrix.api.demo.demo2': {'func': api_demo.demo2},
            'matrix.api.demo.demo3': {'func': api_demo.demo3},
            'matrix.api.demo.demo4': {'func': api_demo.demo4},
            'matrix.api.demo.demo5': {'func': api_demo.demo5}
        }
}

if __name__ == '__main__':
    pass


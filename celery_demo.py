#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/6/16 22:34
# @Author  : BlackMatrix
# @Site : 
# @File : celery_demo.py
# @Software: PyCharm
import time
from celery import Celery

app = Celery('celery_demo',  backend='redis://xxx.xxx.xxx.xxx:6379/0', broker='redis://xxx.xxx.xxx.xxx:6379/0')


@app.task
def add(x, y):
    return x + y

if __name__ == '__main__':
    result = add.delay(4, 4)
    while not result.ready():
        time.sleep(0.5)
        print('task done: {0}'.format(result.get()))

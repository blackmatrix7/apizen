#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/6/7 下午9:50
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: controller.py
# @Software: PyCharm
from functools import wraps
from app.apizen.methods import do_not_format
from .models import DemoChild, DemoParent
from app.webapi.exceptions import ApiSubExceptions
from app.apizen.types import Integer, String, Float, DateTime

__author__ = 'blackmatix'


def test_decorator(func):
    """
    装饰器，测试使用，无功能
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def save_to_db(data: DemoParent):
    data.save().comit()


class ApiDemo:

    def __init__(self):
        self.value = None

    @staticmethod
    @test_decorator
    def set_user(user_id: Integer, name: String,  datetime: DateTime('%Y-%m-%d %H:%M:%S'), mark: Float=None, age: Integer=19):
        """
        测试装饰器对获取函数参数的影响，及接口参数判断说明
        :param user_id:  用户id，必填，当函数参数没有默认值时，接口认为是必填参数
        :param age:  年龄，必填，原因同上
        :param name:  姓名，非必填，当传入值时，接口取参数默认值传入
        :param mark:  分数
        :param datetime:  分数
        :return:  返回测试结果
        """
        return [
            {'user_id': user_id,  'name': name, 'age': age, 'mark': mark, 'datetime': datetime}
        ]

    # 演示静态方法调用
    @staticmethod
    def set_users(users: list):
        def return_users():
            for user in users:
                yield {'user_id': user.get('user_id'),
                       'name': user.get('name'),
                       'age': user.get('age')}
        return list(return_users())

    # 演示类方法调用
    @classmethod
    def class_method(cls, name):
        """
        类方法调用测试
        :param name:  姓名，
        :return:  返回测试结果
        """
        return {'name': name}

    # 演示实例方法调用
    def instance_func(self, value):
        """
        实例方法调用测试
        :param value:  必填，任意字符串
        :return:  返回测试结果
        """
        self.value = value
        return self.value

    # 演示错误的函数写法
    @staticmethod
    def err_func(self):
        """
        模拟错误的函数写法：声明为静态方法，却还存在参数self
        此时获取函数签名时，会将self作为一个接口的默认参数，如果不传入值会抛出异常
        :param self: 静态方法的参数，没有默认值，必填，不是实例方法的self参数
        :return:  返回self的值
        """
        return self

    # 演示抛出异常
    @staticmethod
    def raise_error():
        """
        接口抛出异常的使用说明，抛出异常信息后，会在返回接口的code中显示对应异常的编号，
        同时，返回的http code 也会根据异常配置中的status_code而改变
        :return:  返回异常信息
        """
        raise ApiSubExceptions.unknown_error

    # 演示自定义异常信息
    @staticmethod
    def custom_error():
        """
        接口抛出异常的使用说明，抛出异常信息后，会在返回接口的code中显示对应异常的编号，
        同时，返回的http code 也会根据异常配置中的status_code而改变
        :return:  返回异常信息
        """
        raise ApiSubExceptions.unknown_error('这是一个自定义异常信息')

    # 演示接口接收任意k/w参数
    @staticmethod
    def send_kwargs(value: str, **kwargs):
        """
        VAR_KEYWORD 参数类型的传值测试，传入任意k/w，会在调用结果中返回
        :param value:  任意字符串
        :param kwargs:  键值对
        :return:  返回调用结果
        """
        return {"value": value, "kwargs": kwargs}

demo = ApiDemo()

if __name__ == '__main__':
    pass

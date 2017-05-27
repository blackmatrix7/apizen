# api zen

快速将python函数转换成webapi。

[TOC]

## 前言

之前有大量的web api开发工作，如果每个web api都需要注册路由，检查请求参数，则需要进行大量的重复工作，同时过多的路由也不便于管理，且不易做到统一的api返回格式。

所以就有这个想法，能否尽快地将一个python的函数转换成web api，不用重复注册路由，不需要对请求的参数进行检查，能统一api返回格式，支持api版本管理，对一些公共层面的异常进行处理(如请求参数缺失)。

同时，希望能尽量减少对函数编写的限制，让尽量多的python函数，尽少甚至不做任何修改，只通过简单的添加一个调用名称，可以直接转换成web api。

web api采用统一的请求url： /api/router/rest ，以method参数区分不同的调用方法，这样接口调用方不需要存储大量的接口地址，只需要存储接口调用的方法名。同时，可以统一在接口路由处，添加接口调用日志、接口调用次数限制、ban掉某些ip等功能。

## 特性

1. 统一的web api入口地址，支持接口版本管理及继承
2. 自动判断请求的参数，自动拦截参数不完整的请求
3. 支持常用接口参数类型的自动判断及转换，自动拦截参数类型错误的请求
4. 统一的web api返回格式，提供接口异常代码及详细的异常信息
5. 在不修改业务代码的前提下，同时支持application/x-www-form-urlencoded、application/json等请求方式
6. 绝大多数python函数可以直接转成为web api，减少接口开发工作量，专注业务逻辑实现

## 依赖

```
dict2xml==1.5
six==1.10.0
tornado==4.5.1
```

## 更新日志

2017.05.17	接口部分参数类型判断（str、int、float、list、dict、tuple）

2017.05.16	接口版本支持多重继承

2017.05.09	接口支持版本继承与管理

2017.05.08	接口返回异常信息时，不再统一返回http code 200

2017.05.05	项目初始提交

## 分支说明

现在暂时有两个分支：

master 分支，通常是能正常运行的代码

develop 分支，绝大多数都是随手写的，可能含有很多未完成的功能，以及写一半的代码

## 安装

建立虚拟环境

```shell
python -m venv venv
```

安装依赖包

```shell
pip install -r requirements.txt
```

激活虚拟环境

```shell
source venv/bin/activate
```

退出虚拟环境

```shell
deactivate
```

## QuickStart

### 编写接口处理函数

框架设计之初，希望尽少减少对接口处理函数的限制，让实现业务的函数能更加自由，但是仍有一些规定需要在编写函数时遵守：

1. 暂时不支持VAR_POSITIONAL类型的参数，即*args
2. 函数的返回结果可以正常的转换成json和xml

简单的示例

```python
@staticmethod
def set_user(user_id: int, name: str, mark: float, age: int=19):
    return [
        {'user_id': user_id,  'name': name, 'age': age, 'mark': mark}
    ]
```

### 使用装饰器

接口路由中，通过函数签名获取接口函数参数，以此判断web api调用请求是否符合接口参数要求。

当使用装饰器时，会导致获取到的函数签名错误（获取到装饰器的函数签名），从而无法正常判断接口所需参数。

所以在编写装饰器时，需要在包装器函数上增加一个functools中内置的装饰器 wraps，才能获取正确的函数签名。

```python
from functools import wraps

def test_decorator(func):
    # 需要在包装器函数上增加一个functools中内置的装饰器 wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 判断接口参数类型

接口路由可以通过Type Hints判断请求参数的类型是否符合要求（Python 3.5 PEP0484）。

对于需要做参数类型检查的函数，需要在参数后标记参数类型，目前能对str、int、float、list、dict、tuple这6种类型做参数检查和部分情况下的转换，其他不支持的类型或无法转换的情况，会直接将参数值传给接口处理函数。

如函数示例中的参数age: int，会对参数是否是int进行检查，如果不是，则尝试转换成int，如果转换失败，会抛出code为1022，参数类型错误的异常。

示例，传入一个浮点型的年龄参数（age=12.2）：

http://127.0.0.1:8010/api/router/rest?v=1.0&method=matrix.api.set-user&user_id=11&age=12.2&name=jack&mark=92.5

接口返回参数类型异常，提示age应该为int型

```json
{
    "respone": null,
    "meta": {
        "code": 1022,
        "message": "参数类型错误：age <int>"
    }
}
```

对于list、dict、tuple的参数类型，如果请求的参数是字符串，接口路由会尝试作为json字符串进行解析，解析失败会抛出json格式异常的错误，解析成功则比对是否符合参数类型要求，若解析后仍不符合，则抛出参数类型错误的异常。tuple类型会先由json.loads()转换为list，再转换为tuple，不建议标记参数类型为tuple，会增加额外的类型转换。

### 添加调用方法

在webapi/methods.py中添加接口方法名对应的函数。

每个接口版本为独立的一个类，必须继承自超类ApiMethodBase。

类属性api_methods为dict，表示这个接口版本支持的接口名称与对应方法。

```python
@version('1.0')
class ApiMethodV10(ApiMethodBase):
    api_methods = {
        'matrix.api.err-func': {'func': api_demo.err_func},
        'matrix.api.instance-func': {'func': api_demo.instance_func},
        'matrix.api.send-kwargs': {'func': api_demo.send_kwargs},
        'matrix.api.raise-error': {'func': api_demo.raise_error},
        'matrix.api.only-post': {'func': api_demo.raise_error, 'method': ['post']},
        'matrix.api.api-stop': {'func': api_demo.raise_error, 'enable': False}
    }
```

1. 'matrix.api.instance-func'为接口的方法名
2. 'func'为调用接口后需要执行的python函数
3. ’method‘为接口支持的请求方式，不写method的情况下，默认为同时支持get和post方法。以不支持的请求方式调用接口，会返回1019，不支持的http请求方式的异常
4. ’enable’为接口方法的启用与禁用，不写enable的情况下，默认为True，即接口启用。调用禁用的接口时，会返回1016，api已停用的异常

### 接口版本继承

接口支持版本管理与继承，通过装饰器@version('1.0')注册这个类对应的版本号。

类继承关系即接口继承关系

```python
class ApiMethodBase(metaclass=ApiMethodMeta):
    api_methods = {}
    support_methods = {
        'matrix.api.get-user': {'func': api_demo.get_user},
        'matrix.api.return-err': {'func': api_demo.raise_error}
    }


@version('1.0')
class ApiMethodV10(ApiMethodBase):
    api_methods = {
        'matrix.api.err-func': {'func': api_demo.err_func},
        'matrix.api.instance-func': {'func': api_demo.instance_func},
        'matrix.api.send-kwargs': {'func': api_demo.send_kwargs},
        'matrix.api.raise-error': {'func': api_demo.raise_error},
        'matrix.api.only-post': {'func': api_demo.raise_error, 'method': ['post']},
        'matrix.api.api-stop': {'func': api_demo.raise_error, 'enable': False}
    }
```

上述例子中，声明类ApiMethodV10，继承自超类ApiMethodBase，这样ApiMethodV10支持的类方法，除了自身support_methods的方法外，还会继承来自ApiMethodBase中support_methods的方法。

等价于

```python
@version('1.0')
class ApiMethodV10(ApiMethodBase):
    api_methods = {
        'matrix.api.get-user': {'func': api_demo.get_user},
        'matrix.api.return-err': {'func': api_demo.raise_error}
        'matrix.api.err-func': {'func': api_demo.err_func},
        'matrix.api.instance-func': {'func': api_demo.instance_func},
        'matrix.api.send-kwargs': {'func': api_demo.send_kwargs},
        'matrix.api.raise-error': {'func': api_demo.raise_error},
        'matrix.api.only-post': {'func': api_demo.raise_error, 'method': ['post']},
        'matrix.api.api-stop': {'func': api_demo.raise_error, 'enable': False}
    }
```

这样，每次新增接口版本时，只需要在接口版本对应的类中，编辑类属性support_methods，填写新版本的接口改动情况，会自动继承超类接口版本的接口方法。

### 接口版本禁用

需要禁用某个版本时，在@version装饰器中，新增一个参数enable=False，如

```python
@version('1.0', enable=False)
class ApiMethodV10(ApiMethodBase):
    support_methods = {
        'matrix.api.err-func': {'func': api_demo.err_func},
        'matrix.api.instance-func': {'func': api_demo.instance_func},
        'matrix.api.send-kwargs': {'func': api_demo.send_kwargs},
        'matrix.api.raise-error': {'func': api_demo.raise_error},
        'matrix.api.api-stop': {'func': api_demo.raise_error, 'enable': False}
    }
```

此时，再调用这个接口版本时，会返回接口版本已停用的异常信息。

### 接口异常配置

接口异常信息在exception.py中，分为公共异常和业务异常。

公共异常写在类ApiSysExceptions中，类属性即为异常信息，异常信息为dict，分别有四个参数：

| 参数          | 说明                  | 必填   | 默认值       |
| ----------- | ------------------- | ---- | --------- |
| err_code    | 接口异常时返回的代码，内置部分异常信息 | 是    | 无         |
| status_code | 接口出现异常时返回的http code | 否    | 500       |
| message     | 接口异常说明文字            | 是    | 无         |
| ex_type     | 接口异常类型              | 否    | Exception |

示例

```python
# API 系统层面异常信息，以1000开始
class ApiSysExceptions(ApiBaseExceptions):
    # code 1000 为保留编码，代表执行成功
    # 服务不可用
    missing_system_error = {'api_code': 1001, 'http_code': 403, 'api_msg': '服务不可用', 'ex_type': Exception}
    # 限制时间内调用失败次数
    app_call_limited = {'api_code': 1002, 'http_code': 403, 'api_msg': '限制时间内调用失败次数', 'ex_type': Exception}
    # 请求被禁止
    forbidden_request = {'api_code': 1003, 'http_code': 403, 'api_msg': '请求被禁止', 'ex_type': Exception}
    # 缺少版本参数
    missing_version = {'api_code': 1004, 'http_code': 400, 'api_msg': '缺少版本参数', 'ex_type': KeyError}
```

业务异常写在类ApiSubExceptions中，以2001开始，由具体业务开发定义，配置过程与公共异常相同。

```python
# API 子系统（业务）层级执行结果，以2000开始
class ApiSubExceptions(ApiBaseExceptions):
    empty_result = {'api_code': 2000, 'http_code': 200, 'api_msg': '查询结果为空', 'ex_type': Exception}
    unknown_error = {'api_code': 2001, 'http_code': 500, 'api_msg': '未知异常', 'ex_type': Exception}
    other_error = {'api_code': 2002, 'http_code': 500, 'api_msg': '其它异常', 'ex_type': Exception}
```

## 接口调用测试

运行run.py

**测试装饰器对获取函数参数的影响，及接口参数判断说明**

http://127.0.0.1:8010/api/router/rest?v=1.0&method=matrix.api.set-user&user_id=11&age=12&name=jack&mark=92.5

接口处理函数

```python
@staticmethod
@test_decorator
def set_user(user_id: int, name: str, mark: float, age: int=19):
    """
    测试装饰器对获取函数参数的影响，及接口参数判断说明
    :param user_id:  用户id，必填，当函数参数没有默认值时，接口认为是必填参数
    :param age:  年龄，必填，原因同上
    :param name:  姓名，非必填，当传入值时，接口取参数默认值传入
    :param mark:  分数
    :return:  返回测试结果
    """
    return [
        {'user_id': user_id,  'name': name, 'age': age, 'mark': mark}
    ]
```

返回

```json
{
    "respone": [
        {
            "user_id": 11,
            "mark": 92.5,
            "age": 12,
            "name": "jack"
        }
    ],
    "meta": {
        "code": 1000,
        "message": "执行成功"
    }
}
```

**JSON格式调用方式**

支持Content-Type为application/json的POST请求

http://127.0.0.1:8010/api/router/rest?v=1.0&method=matrix.api.set-user

接口处理函数，同上

POST数据

```json
{
    "user_id": 75,
    "age": 27,
    "name": "李飞飞"
}
```

接口返回

```json
{
    "meta": {
        "code": 1000,
        "message": "执行成功"
    },
    "respone": [
        {
            "age": 27,
            "name": "李飞飞",
            "user_id": 75
        }
    ]
}
```

http://127.0.0.1:8010/api/router/rest?v=1.0&method=matrix.api.set-users

接口处理函数

```python
@staticmethod
def set_users(users: list):
    def return_users():
        for user in users:
            yield {'user_id': user.get('user_id'),  
                   'name': user.get('name'), 
                   'age': user.get('age')}
    return list(return_users())
```

POST数据

```json
{
    "users": [
        {
            "id": 1,
            "age": 22,
            "name": "张三"
        },
        {
            "id": 2,
            "age": 23,
            "name": "李四"
        },
        {
            "id": 3,
            "age": 24,
            "name": "王五"
        }
    ]
}
```

接口返回

```json
{
    "respone": [
        {
            "user_id": null,
            "age": 22,
            "name": "张三"
        },
        {
            "user_id": null,
            "age": 23,
            "name": "李四"
        },
        {
            "user_id": null,
            "age": 24,
            "name": "王五"
        }
    ],
    "meta": {
        "code": 1000,
        "message": "执行成功"
    }
}
```

**实例方法调用**

http://127.0.0.1:8010/api/router/rest?v=1.0&method=matrix.api.instance-func&value=123

接口处理函数

```python
def instance_func(self, value):
    """
    实例方法调用测试
    :param value:  必填，任意字符串
    :return:  返回测试结果
    """
    self.value = value
    return self.value
```

返回

```json
{
    "meta": {
        "message": "执行成功",
        "code": 1000
    },
    "respone": "123"
}
```

**类方法调用**

http://127.0.0.1:8010/api/router/rest?v=1.0&method=matrix.api.class-func&name=jim

接口处理函数

```python
@classmethod
def class_method(cls, name):
    """
    类方法调用测试
    :param name:  姓名，
    :return:  返回测试结果
    """
    return {'name': name}
```

返回

```json
{
    "respone": {
        "name": "jim"
    },
    "meta": {
        "code": 1000,
        "message": "执行成功"
    }
}
```

**不规范函数写法：声明为静态方法，却还存在参数self**

http://127.0.0.1:8010/api/router/rest?v=1.0&method=matrix.api.err-func

接口处理函数

```python
@staticmethod
def err_func(self):
    """
    模拟错误的函数写法：声明为静态方法，却还存在参数self
    此时获取函数签名时，会将self作为一个接口的默认参数，如果不传入值会抛出异常
    :param self: 静态方法的参数，没有默认值，必填，不是实例方法的self参数
    :return:  返回self的值
    """
    return self
```

返回

```json
{
    "meta": {
        "message": "缺少方法所需参数:self",
        "code": 1018
    },
    "respone": null
}
```

**VAR_KEYWORD 参数类型的传值测试**

含有VAR_KEYWORD类型的参数时，框架除了会将全部的k/v作为参数传入，包括框架层面的公共参数，如method、v。

同时此示例演示版本继承的效果，如改成v 1.0无法提示方法不存在，改成v 1.1 v 1.2可以正常访问接口。

http://127.0.0.1:8010/api/router/rest?v=1.1&method=matrix.api.send-kwargs&user_id=11&age=12&value=1

接口处理函数

```python
@staticmethod
def send_kwargs(value: str, **kwargs):
    """
    VAR_KEYWORD 参数类型的传值测试，传入任意k/wc，会在调用结果中返回
    :param value:  任意字符串
    :param kwargs:  键值对
    :return:  返回调用结果
    """
    return {"value": value, "kwargs": kwargs}
```

返回

```json
{
    "respone": {
        "value": "1",
        "kwargs": {
            "method": "matrix.api.send-kwargs",
            "age": "12",
            "v": "1.1",
            "user_id": "11"
        }
    },
    "meta": {
        "message": "执行成功",
        "code": 1000
    }
}
```

**抛出特定异常**

http://127.0.0.1:8010/api/router/rest?v=1.1&method=matrix.api.raise-error

接口处理函数

```python
@staticmethod
def raise_error():
    """
    接口抛出异常的使用说明，抛出异常信息后，会在返回接口的code中显示对应异常的编号，
    同时，返回的http code 也会根据异常配置中的status_code而改变
    :return:  返回异常信息
    """
    raise ApiSubError.unknown_error
```

返回

```json
{
    "meta": {
        "code": 2001,
        "message": "未知异常"
    },
    "respone": null
}
```

### 接口公共参数

公共参数调用填写在query string中

| 参数名    | 必填   | 默认值  | 说明                 |
| ------ | ---- | ---- | ------------------ |
| v      | 是    | 无    | 接口版本号，当前为1.0       |
| method | 是    | 无    | 接口方法名              |
| format | 否    | json | 返回的请求格式，支持json、xml |
| 其他参数   | 否    | 无    | 待完成                |

### 接口业务参数

即请求业务接口需求的参数，支持在query string中传入，也支持以key/value的形式传入(application/x-www-form-urlencoded)，同时支持在body中以json格式传入(application/json)。

当接口函数的参数没有默认值时(如示例函数的user_id，age两个参数)，此参数为必填的参数，转换成web api后，调用需要传入与函数参数同名的参数进行请求，如果未传入同名参数则会抛出code为1018的异常，即”缺少方法所需参数“。

当接口函数的参数存在默认值时(如示例函数的name参数)，此参数为非必填参数，转换为web api后，调用可以不传入name的值，接口函数取参数默认值(如示例函数的”刘峰“)。

| 参数名     | 必填   | 默认值  | 说明      |
| ------- | ---- | ---- | ------- |
| user_id | 是    | 无    | 用户id    |
| age     | 是    | 无    | 用户年龄    |
| name    | 否    | 刘峰   | 测试的用户名称 |

## 接口返回

```json
{
    "meta": {
        "message": "执行成功",
        "code": 1000
    },
    "respone": {
        "user_id": "testcode",
        "name": "刘峰",
        "age": 20
    }
}
```

接口返回信息说明

| 参数       | 说明                                 |
| -------- | ---------------------------------- |
| code     | 执行结果编号，调用者可以根据code得知是否执行成功，或进行异常处理 |
| message  | 执行结果异常说明                           |
| response | 接口函数返回值                            |

### 接口异常信息

接口异常信息分为公共异常信息和业务异常信息，公共异常信息以1001开始，业务异常信息以2001开始

### 公共异常信息

| 编号   | 说明               |
| ---- | ---------------- |
| 1001 | 服务不可用            |
| 1002 | 限制时间内调用失败次数      |
| 1003 | 请求被禁止            |
| 1004 | 缺少版本参数           |
| 1005 | 不支持的版本号          |
| 1006 | 非法的版本参数          |
| 1007 | 缺少时间戳参数          |
| 1008 | 非法的时间戳参数         |
| 1009 | 缺少签名参数           |
| 1010 | 无效签名             |
| 1011 | 无效数据格式           |
| 1012 | 缺少方法名参数          |
| 1013 | 不存在的方法名          |
| 1014 | 缺少access_token参数 |
| 1015 | 无效access_token   |
| 1016 | api已经停用          |
| 1017 | 系统处理错误           |
| 1018 | 缺少方法所需参数         |
| 1019 | 不支持的http请求方式     |
| 1020 | 错误的API配置         |
| 1021 | 无效的json格式        |

### 业务异常信息

以实际业务开发为准

## TODO

### 已完成

1. 调整出现异常时，返回的http code
2. 支持xml格式返回数据
3. 接口版本支持多重继承
4. 接口参数类型判断
5. API版本继承性能优化
6. 支持自定义异常的类型

### 近期

1. 加入单元测试

### 中期

1. 完整的oauth 2.0 鉴权方案实现
2. 接口访问日志记录

### 遥远

1. 性能优化
2. 自动生成接口说明文档
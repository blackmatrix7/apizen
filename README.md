# ApiZen

快速将python函数转换成webapi。

[TOC]

## 介绍

### 前言

项目有大量的web api开发工作，如果使用传统的开发方式，需要编写大量的样板代码，如每个web api都需要注册路由，检查请求参数，处理返回结果。

基于上述原因创建ApiZen，目标是能快速将Python函数转换成web api，统一接口入口，不用重复注册路由，统一对请求的参数进行检查，统一api返回格式，支持api版本管理，对一些公共层面的异常进行处理(如请求参数缺失)。

同时，希望能尽量减少对函数编写的限制，让尽量多的python函数，尽少甚至不做任何修改，只通过简单的添加一个调用名称，可以直接转换成web api。

web api采用统一的请求url： /api/router/rest ，以method参数区分不同的调用方法，这样接口调用方不需要存储大量的接口地址，只需要存储接口调用的方法名。并且，可以统一在接口路由处，添加接口调用日志、接口调用次数限制、ban掉某些ip等功能。

### 特性

1. 统一的web api入口地址，支持接口版本管理及继承
2. 自动判断请求的参数，自动拦截参数不完整的请求
3. 支持常用接口参数类型的自动判断及转换，自动拦截参数类型错误的请求
4. 统一的web api返回格式，提供接口异常代码及详细的异常信息
5. 在不修改业务代码的前提下，同时支持application/x-www-form-urlencoded、application/json等请求方式
6. 绝大多数python函数可以直接转成为web api，减少接口开发的样板代码，专注业务逻辑实现

### 更新日志

2017.07.22	支持在配置文件中自定义路由URL

2017.07.03 	调整接口参数的类型判断方式

2017.05.17	接口部分参数类型判断（str、int、float、list、dict、tuple）

2017.05.16	接口版本支持多重继承

2017.05.09	接口支持版本继承与管理

2017.05.08	接口返回异常信息时，不再统一返回http code 200

2017.05.05	项目初始提交

### 分支说明

现在暂时有两个分支：

master 分支，通常是能正常运行的代码

develop 分支，绝大多数都是随手写的，可能含有很多未完成的功能，以及写一半的代码

### 安装

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

先从编写一个最简单的Python函数开始：在 app/demo/controller.py 中编写一个简单的函数。

```python
def first_api():
    return '这是第一个Api例子'
```

### 将函数注册到系统

函数编写完成后，需要注册到系统的接口列表，并为这个函数取一个唯一的接口名称。

演示项目中，选择在app/demo/methods.py中进行注册

```python
from .controller import first_api
class DemoApiMethods(ApiMethodsBase):
    api_methods = {
        # 第一个API
        'matrix.api.first-api': {'func': first_api},
    	......
    }
```

### 启动项目

使用 python manage.py -env=devcfg devserver 命令启动项目

### 访问接口

在浏览器中访问 http://127.0.0.1:8080/api/router/rest?v=1.0&method=matrix.api.first-api 

可以得到接口返回结果，至此一个最简单的接口完成。

```Json
{
    "meta": {
        "code": 1000,
        "message": "执行成功"
    },
    "respone": "这是第一个Api例子"
}
```

## 接口函数

### 接口参数

ApiZen可以将函数的参数自动转换为web api的参数，并对请求时提交的参数进行判断。

判断遵守以下规则：

1. 对于没有默认值的参数，为必填参数
2. 存在默认值的参数为可选参数，当调用者未传入可选参数时，可选参数取默认值

编写一个模拟用户注册的函数，并注册为接口名称 matrix.api.register_user

```python
def register_user(name, age, email=None):
    return {'name': name, 'age': age, 'email': email}
```

通过get进行请求 http://127.0.0.1:8080/api/router/rest?v=1.0&method=matrix.api.register_user

当不传入任何接口参数时，ApiZen抛出缺少参数的异常

```json
{
    "meta": {
        "code": 1018,
        "message": "缺少方法所需参数：name"
    },
    "respone": null
}
```

当传入所有必填参数时，能正常处理接口请求并返回结果。

http://127.0.0.1:8080/api/router/rest?v=1.0&method=matrix.api.register_user&name=tom&age=19

调用示例中，没有传入email，email取默认值None

```json
{
    "meta": {
        "code": 1000,
        "message": "执行成功"
    },
    "respone": {
        "age": 19,
        "email": null,
        "name": "tom"
    }
}
```

### 接口参数合法性

ApiZen不仅可以对请求接口时提交的参数是否完整进行判断，还可以对接口参数值的合法性进行判断。

继续完善之前编写的模拟注册用户接口，引入ApiZen中的参数类型作为参数的类型注解(Type Hints)，用于对参数合法性进行判断，并加入更多的注册信息。

```python
from app.apizen.schema import Integer, String, Float, Dict, DateTime
def register_user_plus(name, age: Integer, birthday: DateTime('%Y/%m/%d'), email=None):
    return {'name': name, 'age': age, 'birthday': birthday, 'email': email}
```

请求接口，注意age传入的值是19.1

 http://127.0.0.1:8080/api/router/rest?v=1.0&method=matrix.api.register_user_plus&name=tom&age=19.1&birthday=2007/12/31

因为age传入的值为19.1，不符合Integer的要求，所以返回异常

```json
{
    "meta": {
        "code": 1022,
        "message": "参数类型错误：age <Integer>"
    },
    "respone": null
}
```

这个例子中，比较特殊的类型是DateTime，在默认情况下，DateTime会采用默认的日期格式'%Y-%m-%d %H:%M:%S'。

不过在设定参数类型提示时，仍可以自定义DateTime格式的类型，如上述例子的DateTime('%Y/%m/%d')，此时会依据自定义的日期格式判断调用者传入的参数是否合法。

**目前支持判断的参数类型**：

**Integer**

对于字符串类型的参数会尝试进行类型转换，转换成功返回转换后结果，转换失败引发ValueError异常

对于float类型的参数不会进行类型转换，避免精度丢失

**String**

将参数转换成字符串并返回

**Float**

将参数转换成浮点型并返回，无法转换时引发ValueError异常

**Dict**

对于json格式的字符串，尝试转换成dict并返回，如无法转换引发JSONDecodeError异常

**List**

对于json格式的字符串，尝试转换成list并返回，如无法转换引发JSONDecodeError异常

**DateTime**

对于字符串类型，根据设置的日期格式，转换成datetime类型并返回，如无法转换则引发ValueError异常

除ApiZen提供的类型外，也支持使用以下的系统内建类型进行判断：int、float、str、list、dict、datetime。

### 参数的限制

除ApiZen提供的类型外，也支持使用以下的系统内建类型进行判断：int、float、str、list、dict。

ApiZen在设计之初，希望尽少减少对接口处理函数的限制，让实现业务的函数能更加自由，但是仍有一些规定需要在编写函数时遵守：

1. 暂时不支持VAR_POSITIONAL类型的参数，即*args
2. 函数的返回结果可以正常的转换成json

### 使用装饰器

ApiZen通过函数签名获取接口函数参数，以此判断web api调用请求是否符合接口参数要求。

当使用装饰器时，会导致获取到的函数签名错误（获取到装饰器的函数签名），从而无法正常判断接口所需参数。

所以在编写装饰器时，需要在包装器函数上增加一个functools中内置的装饰器 wraps，才能获取正确的函数签名。

```Python
from functools import wraps

def test_decorator(func):
    # 需要在包装器函数上增加一个functools中内置的装饰器 wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

## 接口管理

### 接口版本

接口版本以类的形式存在，每个接口版本为独立的一个类，必须继承自超类ApiMethodBase。

所有接口版本类，都必须调用进行注册。

```python
from app.apizen.version import register
from app.webapi.methods import ApiMethodsV10, ApiMethodsV11
# Web Api 版本注册
register(ApiMethodsV10, ApiMethodsV11)
```

### 接口注册

每个接口版本都必须存在类型属性api_methods，每个接口注册时，向api_methods增加相应的item即可。

```python
@version('1.0')
class ApiMethodV10(ApiMethodBase):
    api_methods = {
        'matrix.api.err-func': {'func': err_func},
        'matrix.api.instance-func': {'func': instance_func},
        'matrix.api.send-kwargs': {'func':send_kwargs},
        'matrix.api.raise-error': {'func': raise_error},
        'matrix.api.only-post': {'func': raise_error, 'method': ['post']},
        'matrix.api.api-stop': {'func':raise_error, 'enable': False}
    }
```

1. 'matrix.api.instance-func'为接口的方法名，同一个函数可以对应多个方法名
2. 'func'为调用接口后需要执行的python函数
3. ’method‘为接口支持的请求方式，不写method的情况下，默认为同时支持get和post方法。以不支持的请求方式调用接口，会返回1019，不支持的http请求方式的异常
4. ’enable’为接口方法的启用与禁用，不写enable的情况下，默认为True，即接口启用。调用禁用的接口时，会返回1016，api已停用的异常

### 接口版本继承

接口支持版本管理与继承，通过装饰器@version('1.0')注册这个类对应的版本号。

类继承关系即接口继承关系

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

## 异常配置

接口异常分为公共异常和业务异常。

异常信息以描述符 ApiException 存储，故所有的系统异常信息都必须以类属性的形式存在。

ApiException接受4个参数，分别为

| 参数        | 说明                  | 必填   | 默认值       |
| --------- | ------------------- | ---- | --------- |
| err_code  | 接口异常时返回的代码，内置部分异常信息 | 是    | 无         |
| http_code | 接口出现异常时返回的http code | 否    | 500       |
| err_msg   | 接口异常说明文字            | 是    | 无         |
| err_type  | 接口异常类型              | 否    | Exception |

### 公共异常

公共异常为框架调用层面的异常，由ApiZen统一提供和管理。

当前版本，公共异常信息在app/apizen/exceptions.py下。

```python
# API 系统层面异常信息
class ApiSysExceptions:
    # code 1000 为保留编码，代表执行成功，异常信息以1001开始
    # 服务不可用
    missing_system_error = ApiException(err_code=1001, http_code=403, err_msg='服务不可用', err_type=Exception)
    # 限制时间内调用失败次数
    app_call_limited = ApiException(err_code=1002, http_code=403, err_msg='限制时间内调用失败次数', err_type=Exception)
    # 请求被禁止
    forbidden_request = ApiException(err_code=1003, http_code=403, err_msg='请求被禁止', err_type=Exception)
    # 缺少版本参数
    missing_version = ApiException(err_code=1004, http_code=400, err_msg='缺少版本参数', err_type=KeyError)
    # 不支持的版本号
    unsupported_version = ApiException(err_code=1005, http_code=400, err_msg='不支持的版本号', err_type=ValueError)
```

### 业务异常

业务异常的存储位置可由具体的业务场景定制。业务异常的代码以2001开始，配置过程与公共异常相同。

```python
# API 子系统（业务）层级执行结果，以2000开始
class ApiSubExceptions:
    empty_result = ApiException(err_code=2000, http_code=200, err_msg='查询结果为空', err_type=Exception)
    unknown_error = ApiException(err_code=2001, http_code=500, err_msg='未知异常', err_type=Exception)
    other_error = ApiException(err_code=2002, http_code=500, err_msg='其它异常', err_type=Exception)
    user_not_exits = ApiException(err_code=2003, http_code=404, err_msg='用户不存在', err_type=Exception)
    wrong_password = ApiException(err_code=2004, http_code=400, err_msg='用户名或密码错误', err_type=Exception)
    email_registered = ApiException(err_code=2005, http_code=400, err_msg='邮箱已注册', err_type=Exception)
```

### 抛出异常

在实际业务实现中，可以如下方式直接抛出异常

```python
from app.webapi.exceptions import ApiSubExceptions
def raise_error():
	raise ApiSubExceptions.unknown_error
```

### 自定义异常内容

上述的异常中，异常代码、异常信息都是预先设定好的。

对于临时需要改变异常内容的情况，在抛出异常时，可以在异常中传入需要自定义的异常信息。

```python
from app.webapi.exceptions import ApiSubExceptions
def custom_error(msg):
	raise ApiSubExceptions.unknown_error('自定义异常文字')
```

## 接口请求

### 请求的参数

接口请求的参数，分为公共参数和业务参数。

#### 公共参数

公共参数是ApiZen用于判断请求接口、版本号、权限验证等所需的参数。

所有的公共参数以query string传递，目前支持以下参数：

| 参数名    | 必填   | 默认值  | 说明               |
| ------ | ---- | ---- | ---------------- |
| v      | 是    | 无    | 接口版本号，当前为1.0     |
| method | 是    | 无    | 接口方法名            |
| format | 否    | json | 返回的请求格式，目前支持json |
| 其他参数   | 否    | 无    | 待完成              |

#### 业务参数

业务参数即每个接口处理函数实现业务逻辑所需的参数。业务参数的配置在上文“接口参数”的设定当中已有详细的说明，不再复述。

业务参数根据接口设定，可以通过querystring或者formdata的形式传递，也可以支持以json的形式传递。

### 两种Content-Type

对于POST的请求方式，在不改动业务代码的前提下，可以同时支持application/json和application/x-www-form-urlencoded两种Content-Type。

#### application/x-www-form-urlencoded

在form data中，以key/value的形式传递接口业务参数。

在此种请求方式下，接口函数的每个参数，都和form data中的key进行匹配。

#### application/json

在body中，以json格式传递接口业务参数。

在此中请求方式下，传入的json格式会被转换成dict，dict第一层的每个key与接口函数参数的名称匹配。

http://127.0.0.1:8080/api/router/rest?v=1.0&method=matrix.api.set-user

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
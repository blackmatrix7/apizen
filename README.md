# func2webapi
快速将python函数转换成webapi

### 特性

1. 统一的web api地址，支持接口版本管理
2. 接口参数自动判断，拦截参数不完整的请求
3. 统一的web api返回格式，提供接口异常代码及详细的异常信息
4. 同时支持application/x-www-form-urlencoded和application/json的请求方式，即支持以key/value的形式传参，也支持以json格式传参
5. 绝大多数python函数可以直接转成为web api，减少接口开发工作量，专注业务逻辑实现

### 依赖

```
tornado==4.5.1
```

### 更新日志

2017.05.15 项目初始提交

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

### 使用方法

#### 编写业务函数

函数要求：

1. 不能含有以下参数名 access_token, method, app_key, sign, timestamp, response_format, v, client_id
2. 暂不支持VAR_POSITIONAL类型的参数，即*args
3. 返回结果可正常转换成json或xml

函数示例：

```python
    @staticmethod
    def demo1(user_id, age, name='刘峰'):
        return {
            'user_id': user_id,
            'name': name,
            'age': age
        }
```

#### 添加调用方法

在webapi/api_list.py中添加函数调用名称，如

```python
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
```

”1.0”为接口版本号，matrix.api.demo.demo1为接口方法名，{'func': api_demo.demo1} 为需要调用的函数对象。

#### 接口调用

运行run.py

访问 http://127.0.0.1:8010/api/router/rest?v=1.0&method=matrix.api.demo.demo1 调用接口

##### 接口公共参数

公共参数调用填写在query string中

| 参数名             | 必填   | 默认值  | 说明                 |
| --------------- | ---- | ---- | ------------------ |
| v               | 是    | 无    | 接口版本号，当前为1.0       |
| method          | 是    | 无    | 接口方法名              |
| response_format | 否    | json | 返回的请求格式，支持json或xml |
| 其他参数            | 否    | 无    | 待完成                |

##### 接口业务参数

即请求业务接口需求的参数，支持在query string中传入，也支持以key/value的形式传入(application/x-www-form-urlencoded)，同时支持在body中以json格式传入(application/json)。

接口函数示例

```python
    @staticmethod
    def demo1(user_id, age, name='刘峰'):
        return {
            'user_id': user_id,
            'name': name,
            'age': age
        }
```

当接口函数的参数没有默认值时(如示例函数的user_id，age两个参数)，此参数为必填的参数，转换成web api后，调用需要传入与函数参数同名的参数进行请求，如果未传入同名参数则会抛出code为1018的异常，即”缺少方法所需参数“。

当接口函数的参数存在默认值时(如示例函数的name参数)，此参数为非必填参数，转换为web api后，调用可以不传入name的值，接口函数取参数默认值(如示例函数的”刘峰“)。

| 参数名     | 必填   | 默认值  | 说明      |
| ------- | ---- | ---- | ------- |
| user_id | 是    | 无    | 用户id    |
| age     | 是    | 无    | 用户年龄    |
| name    | 否    | 刘峰   | 测试的用户名称 |

#### 接口返回

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
| message  | 执行结构异常说明                           |
| response | 接口函数返回值                            |

##### 接口异常信息

接口异常信息分为公共异常信息和业务异常信息，公共异常信息以1001开始，业务异常信息以2001开始

公共异常信息

| 编号   | 说明                    |
| ---- | --------------------- |
| 1001 | 服务不可用                 |
| 1002 | 限制时间内调用失败次数           |
| 1003 | 请求被禁止                 |
| 1004 | 缺少版本参数                |
| 1005 | 不支持的版本号               |
| 1006 | 非法的版本参数               |
| 1007 | 缺少时间戳参数               |
| 1008 | 非法的时间戳参数              |
| 1009 | 缺少签名参数                |
| 1010 | 无效签名                  |
| 1011 | 无效数据格式                |
| 1012 | 缺少方法名参数               |
| 1013 | 不存在的方法名               |
| 1014 | 缺少access_token参数      |
| 1015 | 无效access_token        |
| 1016 | api已经停用               |
| 1017 | 系统处理错误                |
| 1018 | 缺少方法所需参数              |
| 1019 | 不支持的http请求方式          |
| 1020 | 错误的API配置              |
| 1021 | 无效的json格式             |
| 1022 | 不支持VAR_POSITIONAL参数类型 |

###### 业务异常信息以实际业务开发为准

### TODO

1. 支持以json或xml格式返回调用结果
2. 完整的oauth 2.0 鉴权方案实现
3. 接口访问日志记录
4. 某些时间段内接口调用次数限制
5. 自动生成接口说明文档


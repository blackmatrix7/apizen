# func2webapi
快速将python函数转换成webapi

### 特性

1. 统一的web api地址，支持接口版本管理
2. 接口参数自动判断
3. 统一的web api返回格式，提供接口异常代码及详细的异常信息
4. 同时支持application/x-www-form-urlencoded和application/json的请求方式，即支持以key/value的形式传参，也支持以json格式传参
5. 绝大多数python函数可以直接转成为web api，减少接口开发工作量，专注业务逻辑实现

### 更新日志

2017.05.15 项目初始提交

### 原理说明

pass

### 安装

```shell
pip install -r requirements.txt
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

### TODO

1. 支持以json或xml格式返回调用结果
2. 完整的oauth 2.0 鉴权方案实现
3. 接口访问日志记录
4. 某些时间段内接口调用次数限制
5. 自动生成接口说明文档


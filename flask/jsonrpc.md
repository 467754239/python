## flask jsonrpc

[jsonrpc api](https://pypi.python.org/pypi/Flask-JSONRPC/0.3.1)

> jsonrpc server端

```
#coding:utf-8
#name:jsonrpc.py

from flask import Flask, request
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api')

# 响应无参数传入的method
@jsonrpc.method('App.index')
def index():
    return 'hello world.'

# 响应有指定参数传入的method
@jsonrpc.method('App.name')
def name(name):
    return 'hello %s.' % name

# 响应有不定参数传入的method，最常用.
@jsonrpc.method('App.user')
def user(**kwargs):
    name = kwargs.get('name')
    age = kwargs.get('age')
    return 'I am %s, age is %s.' % (name, age)

# 如果要传入的参数比较多，kwargs.get()的方式可能比较费劲，
# 可以用get_json()获取所有的参数，通过列表字典的方式减少代码量.
@jsonrpc.method('App.users')
def users(**kwargs):
    # print dir(request)
    # url = request.url
    data = request.get_json()
    # data = {u'jsonrpc': u'2.0', u'params': {u'age': 26, u'name': u'zhengys'}, u'method': u'App.users', u'id': 1}
    name = data['params']['name']
    age = data['params']['age']
    return 'I am %s, age is %s.' % (name, age)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

> jsonrpc client端

```
#coding:utf-8
#name:req_json.py

import json
import requests

url = 'http://localhost:5000/api'
headers = {'Content-Type': 'application/json', 'indent' : 4}

data1 = {
    'jsonrpc' : '2.0',
    'method' : 'App.index',
    'params' : {},
    'id' : 1,
    }

data2 = {
    'jsonrpc' : '2.0',
    'method' : 'App.name',
    'params' : {'name':'zhengys'},
    'id' : 1,
    }

data3 = {
    'jsonrpc' : '2.0',
    'method' : 'App.user',
    'params' : {'name':'zhengys', 'age' : 26},
    'id' : 1,
    }

data4 = {
    'jsonrpc' : '2.0',
    'method' : 'App.users',
    'params' : {'name':'zhengys', 'age' : 26},
    'id' : 1,
    }


# 替换data4,分别为data1, data2, data3.
req = requests.post(url=url, headers=headers, data=json.dumps(data4))   
print req.status_code
print req.content
```
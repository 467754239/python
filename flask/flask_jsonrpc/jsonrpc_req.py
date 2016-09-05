#coding:utf-8

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
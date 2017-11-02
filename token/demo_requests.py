#!/usr/bin/env python
#coding:utf-8

import json
import requests

# 模拟登陆并生成token
url = "http://127.0.0.1:5000/login"
data = {"username":"zhengys", "password":"123456"}
r = requests.post(url, data=data)
print r.status_code
print r.text
if r.status_code == 200:
    ret = json.loads(r.text.encode('utf-8'))
    token = ret['token']
else:
    token = None


# 调用生成的token 进行后面的操作认证。api是无状态的的，先生成一个token，然后用这个token进行后面权限的认证
# web环境中 通过cookie或者session保存状态 在用户登录成功获取到token后可以把token存放在session，然后直接从session中获取到token


# 模拟验证创建的token是否有效
url = "http://127.0.0.1:5000"
params = {"token" : token}
r = requests.get(url, params=params)
print r.status_code
print r.text

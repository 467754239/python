#!/usr/bin/env python
#coding:utf-8

import time
import json
import base64
import random
import hashlib
from flask import Flask, request

'''
1. token是什么？
    官方解释：令牌，代表执行某些操作的权利的对象
    个人理解：用户信息的加密串，系统拿到这个加密串来判断用户是谁，能干什么，不能干什么
2. token怎么生成？
    token的生成方式因人而异，大致思路是将自己需要的一些信息，混合时间戳，随机数等加密生成。我自己的习惯是 (用户名，用户id，角色，时间戳，随机数)
    生成token
        token = base64.b64encode(name|uid|role|str(random.random())|int(time.time()+7200))
3. token怎么用？以判断登录是否过期？
    先解密token，生成一个列表
        res=base64.b64decode(token) 
    通过时间戳判断token是否失效
        if int(res.split('|'))[4] > int(time.time())
            return True
'''

app = Flask(__name__)

# 创建token
def create_token(name, uid, role):
    now = int((time.time())) + 7200 # 2小时后的时间戳
    s = "%s|%s|%s|%s|%s" % (name, uid, role, random.random(), now)
    return base64.b64encode(s)
    
# 验证token
def verify_token( token ):
    now = int((time.time()))
    s = base64.b64decode(token)
    ret = s.split('|')
    if len(ret) < 5:    
        return json.dumps({"code" : 1, "errmsg" : "miss token string."})
    if ret[-1] < now:
        # token已过期 失效
        return json.dumps({"code" : 1, "errmsg" : "token expire."})
    else:
        # 解密后 返回name uid role信息
        return json.dumps({"code" : 0, "username" : ret[0], "uid" : ret[1], "role" : ret[2]})
        
@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "zhengys" and password == "123456":      # 用户密码正确，则生成要给token,实际开发中需要数据库 
        uid, role = 5, 3                                    # 模拟登录成功，从数据库中取到了用户的id,role等信息
        # 如果认证通过则生成token
        token = create_token(username, uid, role)
        ret = json.dumps({"code" : 0, "token" : "%s" % token})
    else:
        ret = json.dumps({"code" : 1, "token" : "token create failed."})
    return ret
        

@app.route("/", methods=['GET', 'POST'])
def index():
    token = request.args.get("token")
    ret = verify_token(token)
    ret = json.loads(ret)
    if int(ret['code']) == 1:
        return "errmsg : %s" % ret['token']
    if int(ret['role']) == 0:
        return "%s is admin, you can do everything" % ret['username']
    else:
        return "%s is not admin, requests failed" % ret['username']
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

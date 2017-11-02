#!/usr/bin/env python
#coding:utf-8

import time
import json
import base64
import random
import hashlib
from flask import Flask, request

'''
1. token��ʲô��
    �ٷ����ͣ����ƣ�����ִ��ĳЩ������Ȩ���Ķ���
    ������⣺�û���Ϣ�ļ��ܴ���ϵͳ�õ�������ܴ����ж��û���˭���ܸ�ʲô�����ܸ�ʲô
2. token��ô���ɣ�
    token�����ɷ�ʽ���˶��죬����˼·�ǽ��Լ���Ҫ��һЩ��Ϣ�����ʱ�����������ȼ������ɡ����Լ���ϰ���� (�û������û�id����ɫ��ʱ����������)
    ����token
        token = base64.b64encode(name|uid|role|str(random.random())|int(time.time()+7200))
3. token��ô�ã����жϵ�¼�Ƿ���ڣ�
    �Ƚ���token������һ���б�
        res=base64.b64decode(token) 
    ͨ��ʱ����ж�token�Ƿ�ʧЧ
        if int(res.split('|'))[4] > int(time.time())
            return True
'''

app = Flask(__name__)

# ����token
def create_token(name, uid, role):
    now = int((time.time())) + 7200 # 2Сʱ���ʱ���
    s = "%s|%s|%s|%s|%s" % (name, uid, role, random.random(), now)
    return base64.b64encode(s)
    
# ��֤token
def verify_token( token ):
    now = int((time.time()))
    s = base64.b64decode(token)
    ret = s.split('|')
    if len(ret) < 5:    
        return json.dumps({"code" : 1, "errmsg" : "miss token string."})
    if ret[-1] < now:
        # token�ѹ��� ʧЧ
        return json.dumps({"code" : 1, "errmsg" : "token expire."})
    else:
        # ���ܺ� ����name uid role��Ϣ
        return json.dumps({"code" : 0, "username" : ret[0], "uid" : ret[1], "role" : ret[2]})
        
@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "zhengys" and password == "123456":      # �û�������ȷ��������Ҫ��token,ʵ�ʿ�������Ҫ���ݿ� 
        uid, role = 5, 3                                    # ģ���¼�ɹ��������ݿ���ȡ�����û���id,role����Ϣ
        # �����֤ͨ��������token
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

#!/usr/bin/env python
#coding:utf-8

import json
import requests

# ģ���½������token
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


# �������ɵ�token ���к���Ĳ�����֤��api����״̬�ĵģ�������һ��token��Ȼ�������token���к���Ȩ�޵���֤
# web������ ͨ��cookie����session����״̬ ���û���¼�ɹ���ȡ��token����԰�token�����session��Ȼ��ֱ�Ӵ�session�л�ȡ��token


# ģ����֤������token�Ƿ���Ч
url = "http://127.0.0.1:5000"
params = {"token" : token}
r = requests.get(url, params=params)
print r.status_code
print r.text

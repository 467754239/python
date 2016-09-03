#coding:utf-8


import json
import requests


# GET
req = requests.get(url)
print req.status_code
print req.content

params = {'username':'zhengys', 'passwd':'123456'}
req = requests.get(url, params=params)
print req.status_code
print req.content


# POST
headers = {'content-type': 'application/json'}
data = {'name' : 'zhengys', 'age' : 26, 'region' : 'cn'}
req = requests.post(url, json=data, headers=headers, timeout=5)
req = requests.post(url, data=json.dumps(data), headers=headers, timeout=5)
print req.status_code
print req.content


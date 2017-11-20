#coding:utf-8


import os
import sys
import time
import json
import base64
import requests
from datetime import datetime
import threading


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



# interface
url = 'http://xx.xx.xx.xx:8000/voice/device/uploadAlarmInfo.json'

data = {'uuid':'voice-test-jx-1', 'alarmType':1, 'timeDuration':10}
headers = {'Content-type': 'multipart/form-data'}

files = {'recordingFile': open('/home/ec2-user/voice/123.mp3', 'rb')}

def req():
    req = requests.post(url, files=files, data=data, verify=False)
    print req.status_code
    print req.content
    time.sleep(1)


threads = []
for x in xrange(1, int(sys.argv[1])):
    thread = threading.Thread(target=req)
    thread.setDaemon(True)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()


## RESTFUL API客户端封装
```python
import json

import requests


class httpRequest(object):

    def __init__(self):
        self.timeout = 3


    @staticmethod
    def get(url, payload=None):
        '''
        Sends a GET request.
        '''
        req = requests.get(url=url, params=payload)
        return _do(req)


    @staticmethod
    def post(url, payload):
        '''
        Sends a POST request.
        '''
        if isinstance(payload, dict):
            req = requests.post(url, data=payload)
        elif isinstance(payload, list):
            req = requests.post(url, json=payload)
        else:
            return 'method: post, params is error, please check your params.', False
        return _do(req)


    @staticmethod
    def put(url, payload):
        '''
        Sends a PUT request.
        '''
        if isinstance(payload, dict):
            req = requests.put(url, data=payload)
            return _do(req)
        else:
            return 'method: put, params is error, please check your params.', False


    @staticmethod
    def delete(url):
        '''
        Sends a DELETE request.
        '''
        req = requests.delete(url)
        return _do(req)


    @staticmethod
    def options(url):
        '''
        Sends an OPTIONS request.
        '''
        req = requests.options(url)
        return _do(req)


    @staticmethod
    def head(url):
        '''
        Sends an HEAD request.
        '''
        req = requests.options(url)
        return _do(req)


def _do(handler):
    if handler.status_code == 200:
        return _parseException(handler.text), True
    else:
        return _parseException(handler.text), False


def _parseException(response):
    try:
        return json.loads(response)
    except ValueError as e:
        return response
    except Exception as e:
        return e.args




if __name__ == '__main__':
    response = httpRequest.get(url="http://www.baidu.com/")
    print response
```

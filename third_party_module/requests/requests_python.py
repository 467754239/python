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
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import time
import random
import socket
import logging

# 单位
unit = {'K' : 1, 'M' : 2 ** 10, 'G' : 2 ** 20, 'T' : 2 ** 30}  

def getHost():
    return socket.gethostname()

def getLoadAvg():
    with open('/proc/loadavg', 'r') as f:
        loadavg = f.readline().split()[0:3]
        return loadavg[0]

def getMemTotal():
    with open('/proc/meminfo', 'r') as f:
        MemTotal = f.readline().split()[1]
        return MemTotal

def getMemUsage(noBufferCache=True):
    with open('/proc/meminfo', 'r') as f:
        data = f.read()
        T = int(re.findall(r'MemTotal:\s+\d+', data)[0].split()[1])                # total
        F = int(re.findall(r'MemFree:\s+\d+', data)[0].split()[1])                 # free
        B = int(re.findall(r'Buffers:\s+\d+\s', data)[0].split()[1])               # buffer
        C = int(re.findall(r'[^a-zA-Z](Cached:\s+\d+\s)', data)[0].split()[1])     # cached
        
        if noBufferCache:
            MemUsage = T - F - B - C
        else:
            MemUsage = T - F
    return MemUsage

def getMemFree(noBufferCache=True):
    with open('/proc/meminfo', 'r') as f:
        data = f.read()
        T = int(re.findall(r'MemTotal:\s+\d+', data)[0].split()[1])                # total
        F = int(re.findall(r'MemFree:\s+\d+', data)[0].split()[1])                 # free
        B = int(re.findall(r'Buffers:\s+\d+\s', data)[0].split()[1])               # buffer
        C = int(re.findall(r'[^a-zA-Z](Cached:\s+\d+\s)', data)[0].split()[1])     # cached

        if noBufferCache:
            MemFree = F + B + C
        else:
            MemFree = int(re.findall(r'MemFree:\s+\d+', data)[0].split()[1])       # free
    return MemFree

def getTime():
    return int(time.time())

def format(num):
    for k, v in unit.items():
        t = float(num) / v
        if t >= 1 and t < 1024:
            return '%s%s' % (round(t, 2), k)
    return

def runAllGet():
    msgInfo = {
        'Host' : getHost(),
        'LoadAvg' : getLoadAvg() ,
        'MemTotal' : int(getMemTotal()) / 1024 ,
        'MemUsage' :int( getMemUsage()) / 1024  ,
        'MemFree' : int(getMemFree()) / 1024 ,
        'Time' : getTime(),
        'user_define' : random.randint(1, 1000)
        }
    return msgInfo

if __name__ == '__main__':
    runAllGet()
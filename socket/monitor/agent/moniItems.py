# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import os
import time
import socket
import logging

# 设置最小单位为k
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

def getMemUsage():
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

def getMemFree():
    if noBufferCache:
        with open('/proc/meminfo', 'r') as f:
            data = f.read()
            T = int(re.findall(r'MemTotal:\s+\d+', data)[0].split()[1])                # total
            F = int(re.findall(r'MemFree:\s+\d+', data)[0].split()[1])                 # free
            B = int(re.findall(r'Buffers:\s+\d+\s', data)[0].split()[1])               # buffer
            C = int(re.findall(r'[^a-zA-Z](Cached:\s+\d+\s)', data)[0].split()[1])     # cached
            MemFree = F + B + C
    else:
        with open('/proc/meminfo', 'r') as f:
            data = f.read()
            F = int(re.findall(r'MemFree:\s+\d+', data)[0].split()[1])                 # free
            MemFree =  F
    return MemFree

def getDisk():
    f = os.popen('sudo fdisk -l')
    data = f.read()
    f.close()
    disks_unit = self._formatDisk(data)
    return { k : self.formatNum(v) for k, v in disks_unit.items() }

def getCpuNum():
    # physics cpu nums
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line.startswith('physical id'):
                 cpu_num = line.split(':')[1]
    return int(cpu_num) + 1

def getTime():
    return int(time.time())

def format(num):
    for k, v in unit.items():
        t = float(num) / v
        if t >= 1 and t < 1024:
            return '%s%s' % (round(t, 2), k)
    return

def format_disk():
    pass

def runAllGet():
    msgInfo = {
            'LoadAvg' : random.randint(1, 1000),
            'MemTotal' : random.randint(1, 1000),
            'MemFree' : random.randint(1, 1000),
            'MemUsage' : random.randint(1, 1000),
            'Time' : int(time.time()),
            'Host' : 'zhengys',
            'user_define' : random.randint(1, 1000)
            }
    return msgInfo

if __name__ == '__main__':
    runAllGet()
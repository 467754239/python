# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import time
import random
import socket
import logging
import subprocess

import psutil

'''
1. 主机名
2. 内存
3. ip与mac地址
4. cpu信息(cpu的型号model name)
5. 硬盘分区信息
6. 制造商信息
7. 出厂日期
8. 系统版本
'''

def get_hostname():
    return socket.gethostname()

def get_loadavg():
    with open('/proc/loadavg', 'r') as f:
        loadavg = f.readline().split()[0:3]
        return loadavg[0]

def get_mem_info(noBufferCache=True):
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith('MemTotal'):
                mem_total = int(line.split(':')[1].split()[0])
            elif line.startswith('MemFree'):
                mem_free = int(line.split(':')[1].split()[0])
            elif line.startswith('Buffers'):
                mem_buffer = int(line.split(':')[1].split()[0])
            elif line.startswith('Cached'):
                mem_cached = int(line.split(':')[1].split()[0])

        if noBufferCache:
            usage = mem_total - mem_free - mem_buffer - mem_cached
            free = mem_free + mem_buffer + mem_cached
        else:
            free = mem_free
            usage = mem_total - mem_free

        return {'mem_total':mem_total, 'mem_free':free, 'mem_usage':usage}

def get_cpu_info():
    cpu_info = {'cpu num' : 0, 'cpu model' : None}
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line.startswith('processor'):
                cpu_info['cpu num'] += 1
            elif line.startswith('model name'):
                cpu_info['cpu model'] = line.split(':')[1].strip()
    return cpu_info

def get_device_info():
    device_white = ['eth0', 'eth1']
    ret = []

    for device, info in psutil.net_if_addrs().items():
        if device in device_white:
            for snic in info:
                if snic.family == 2:
                    ip = snic.address
                elif snic.family == 17:
                    mac = snic.address
            ret.append({'ip' : ip, 'mac' : mac})
    return ret

def get_manufacturer():
    pass

def get_rel_data():
    pass

def get_os_version():
    pass

def get_time():
    return int(time.time())

def format(num):
    unit = {'K' : 1, 'M' : 2 ** 10, 'G' : 2 ** 20, 'T' : 2 ** 30}  
    for k, v in unit.items():
        t = float(num) / v
        if t >= 1 and t < 1024:
            return '%s%s' % (round(t, 2), k)
    return

def main():
    print get_hostname()
    print get_loadavg()
    print get_mem_info()
    print get_cpu_info()
    print get_device_info()

if __name__ == '__main__':
    main()
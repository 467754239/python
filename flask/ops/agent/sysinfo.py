# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import os
import sys
import time
import socket
import getpass
import logging
import datetime
import subprocess
from pwd import getpwnam

import requests

reload(sys) 
sys.setdefaultencoding('utf-8')

# 返回当前用户的UID.
def get_current_uid():
    return getpwnam(getpass.getuser())[2]

# 返回主机名.
def get_hostname():
    return socket.gethostname()

# 返回操作系统信息.
def get_osinfo():
    os_val = os.uname()
    return {'os_type' : os_val[0], 'os_kernel' : os_val[2]}

# 返回公网IP.
def get_public_ip():
    url = 'http://members.3322.org/dyndns/getip'
    mincnt = 1
    maxcnt = 10
    while mincnt < maxcnt:
        try:
            req = requests.get(url=url, timeout=15)
            if req.status_code == 200:
                return req.text.rstrip('\n')
        except Exception as e:
            logging.error('request url:%s, failed times:%s, error message:%s.' % (url, mincnt, e))
            mincnt += 1
            time.sleep(0.5)
    return None

# 返回内网IP.
def get_private_ip():
    ipaddr = re.compile(r'(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})){3}')
    p = subprocess.Popen('ifconfig', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    for block in stdout.split('\n\n'):
        if not block.startswith('lo'):
            if ipaddr.search(block):
                return ipaddr.search(block).group()
    return None

# 返回内存及swap大小.
def get_mem_info():
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith('MemTotal'):
                memtotal = line.split()[1]
            elif line.startswith('SwapTotal'):
                swaptotal = line.split()[1]
    memtotal = change_unit(int(memtotal)*1024)
    swaptotal = change_unit(int(swaptotal)*1024)
    return {'memtotal' : memtotal, 'swaptotal' : swaptotal}

# 返回CPU信息.
def get_cpuinfo():
    cpu_info = {}
    with open('/proc/cpuinfo', 'r') as f:
        core_msg = f.read().split('\n\n')[-2]
        for line in core_msg.split('\n'):
            if line.startswith('processor'):    # 逻辑CPU个数.
                cpu_info['logic_cpu_num'] = int(line.split()[-1]) + 1
            elif line.startswith('model name'):
                cpu_info['model_name'] = line.split(':')[-1].lstrip()
    return cpu_info

# 返回制造商信息.
def get_manufacturer():
    cmd = """/usr/sbin/dmidecode | grep -A6 'System Information'"""
    returncode, stdout = execute_command(cmd)
    if returncode != 0 or not stdout:
        return {'disk_size' : None}

    for line in stdout.split('\n'):
        if 'Manufacturer' in line:          # 制造商
            manufacturer = line.split(':')[1].lstrip()
        elif 'Product Name' in line:        # 产品名称
            product_name = line.split(':')[1].lstrip()
        elif 'Serial Number' in line:       # 序列号
            serial_number = line.split(':')[1].lstrip()
        elif 'UUID' in line:                # uuid
            uuid = line.split(':')[1].lstrip()
    return {'manufacturer' : manufacturer, 'product_name' : product_name, 'serial_number' : serial_number, 'uuid' : uuid}

# 返回磁盘信息.
def get_disk_size():
    returncode, stdout = execute_command('fdisk -l')
    if returncode != 0 or not stdout:
        return {'disk_size' : None}

    for line in stdout.strip().split('\n\n'):
        headline = line.split('\n')[0]
        disk_size = headline.split('MB, ')[1].split()[0]
        if disk_size:
            disk_size = change_unit(disk_size)
            break
    return {'disk_size' : disk_size}

# 返回当前日期时间.
def get_datetime():
    now = datetime.datetime.now()
    return datetime.datetime.strftime(now, "%Y-%m-%d %H:%M:%S")

def change_unit(num):
    unit = {'b' : 1, 'k' : 2**10, 'm' : 2**20, 'g' : 2**30, 't' : 2**40}
    for k, v in unit.items():
        format_num = float(num) / v
        if format_num >= 1 and format_num < 1024:
            return '%s%s' % (round(format_num, 2), k.upper())
    return num

def execute_command(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    returncode = p.returncode
    logging.debug('cmd:%s, return code:%s' % (cmd, returncode))
    return returncode, stdout

def send(data):
    url = 'http://localhost:5000/hostinfo'
    r = requests.post(url=url, json=data, timeout=15)

def main():
    if get_current_uid() != 0:
        print 'Usage: Must be root ro run this script.'
        sys.exit(1)

    data = {}
    data['hostname'] = get_hostname()
    data['public_ip'] = get_public_ip()
    data['private_ip'] = get_private_ip()
    data['update_datetime'] = get_datetime()
    data.update(get_osinfo())
    data.update(get_mem_info())
    data.update(get_cpuinfo())
    data.update(get_manufacturer())
    data.update(get_disk_size())
    print data
    send(data)

if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(filename)s line:%(lineno)d %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    main()


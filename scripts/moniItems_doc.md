## 采集主机信息
> 主机名、系统负载、总计内存、使用内存、空闲内存、多个硬盘总计、当前时间戳  
> 1. 返回值为json
> 2. 单位由k换算成对应的M、G、T单位

```python
#coding:utf-8

import re
import os
import time
import socket
import logging


class hostinfo(object):
    def __init__(self):
        self.unit = {'K' : 1, 'M' : 2 ** 10, 'G' : 2 ** 20, 'T' : 2 ** 30}  # 设置最小单位为k 

    def getHost(self):
        return socket.gethostname()

    def getLoadAvg(self):
        with open('/proc/loadavg', 'r') as f:
            loadavg = f.readline().split()[0:3]
            return loadavg[0] 

    def getMemTotal(self):
        with open('/proc/meminfo', 'r') as f:
            MemTotal = f.readline().split()[1]
            return self.formatNum(MemTotal)

    def getMemUsage(self, noBufferCache=True):
        if noBufferCache:
            with open('/proc/meminfo', 'r') as f:
                data = f.read()
                T = int(re.findall(r'MemTotal:\s+\d+', data)[0].split()[1])                # total
                F = int(re.findall(r'MemFree:\s+\d+', data)[0].split()[1])                 # free
                B = int(re.findall(r'Buffers:\s+\d+\s', data)[0].split()[1])               # buffer
                C = int(re.findall(r'[^a-zA-Z](Cached:\s+\d+\s)', data)[0].split()[1])     # cached
                MemUsage = T - F - B - C
        else:
            with open('/proc/meminfo', 'r') as f:
                data = f.read()
                T = int(re.findall(r'MemTotal:\s+\d+', data)[0].split()[1])                # total
                F = int(re.findall(r'MemFree:\s+\d+', data)[0].split()[1])                 # free
                MemUsage =  T - F
        return self.formatNum(MemUsage)
        
    def getMemFree(self, noBufferCache=True):
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
        return self.formatNum(MemFree)

    def getDisk(self):
        f = os.popen('sudo fdisk -l')
        data = f.read()
        f.close()
        disks_unit = self._formatDisk(data)
        return { k : self.formatNum(v) for k, v in disks_unit.items() }

    def _formatDisk(self, data):
        try:
            if '\xe7\xa3\x81\xe7\x9b\x98' in data:
                # disks = re.findall(r'磁盘\s(/dev/[a-z]{3,}.*\s[A-Z]{2,})', data)             # cn_disk
                tuple_disks = re.findall(r'磁盘\s(/dev/[a-z]{3,}).*\s[A-Z]{2,},\s([0-9]{1,})\s\xe5\xad\x97\xe8\x8a\x82\xef\xbc\x8c', data)
            else:
                # disks = re.findall(r'Disk\s(/dev/[a-z]{4,}:\s[\d.]{1,}\s[A-Z]{1,})', data)   # en_disk
                tuple_disks = re.findall(r'Disk\s(/dev/[a-z]{4,}):\s[\d.]{1,}\s[A-Z]{1,},\s([0-9]{1,})\sbytes', data)
            #return { x.split('\xef\xbc\x9a')[0]:x.split('\xef\xbc\x9a')[1] for x in disks if x }
            return { x[0]:int(x[1])/1000  for x in tuple_disks if x }
        except Exception as e:
            logging.error('format disk result error, %s', e)
            return {} 

    def getTime(self):
        return int(time.time())

    def formatNum(self, num):
        for k, v in self.unit.items():
            t = float(num) / v
            if t >= 1 and t < 1024:
                return '%s%s' % (round(t, 2), k)
        return

    def formatData(self):
        msgInfo = {
                'loadavg' : self.getLoadAvg(),
                'MemTotal' : self.getMemTotal(),
                'MemFree' : self.getMemUsage(),
                'MemUsage' : self.getMemFree(),
                'time' : self.getTime(),
                'host' : self.getHost(),
                }
        msgInfo.update(self.getDisk())
        return msgInfo

if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(filename)s line:%(lineno)d %(levelname)s %(message)s '
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    data = hostinfo().formatData()
    logging.debug('data:%s', data)
```

> 代码执行结果

```python
$ python moniItems.py
WARNING: fdisk GPT support is currently new, and therefore in an experimental phase. Use at your own discretion.
{'MemTotal': '3.68G', 'MemUsage': '3.36G', 'MemFree': '330.45M', '/dev/xvda': '8.19G', 'host': 'ip-172-30-29-108', 'loadavg': '0.00', 'time': 1469238194, '/dev/xvdb': '4.09G'}
2016-07-23 01:43:14,595 moniItems.py line:109 DEBUG data : {'MemTotal': '3.68G', 'MemUsage': '3.36G', 'MemFree': '330.45M', '/dev/xvda': '8.19G', 'host': 'ip-172-30-29-108', 'loadavg': '0.00', 'time': 1469238194, '/dev/xvdb': '4.09G'}
```

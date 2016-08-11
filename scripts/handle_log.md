```
$ head -n 10 access-8000.log
54.222.132.12 - - [2016-08-09T00:15:19+00:00] "POST /user/app/customer/AuthenCross.json HTTP/1.1" 200 213 "-" "Apache-HttpClient/4.5.2 (Java/1.6.0_45)" "-"
54.222.132.12 - - [2016-08-09T00:19:54+00:00] "POST /user/app/customer/getUserInfo.json HTTP/1.1" 200 343 "-" "Apache-HttpClient/4.5.2 (Java/1.6.0_45)" "-"
222.168.25.10 - - [2016-08-09T00:19:55+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=origin.png HTTP/1.1" 404 5 "-" "okhttp/2.6.0" "-"
220.248.15.74 - - [2016-08-09T00:24:56+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=F59B7A3F03317289EFDC9648C4D507B0_motion_1470646715652_small.jpg HTTP/1.1" 200 12996 "-" "snap/1.1.53 CFNetwork/758.5.3 Darwin/15.6.0" "-"
220.248.15.74 - - [2016-08-09T00:24:56+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=F59B7A3F03317289EFDC9648C4D507B0_motion_1470645596591_small.jpg HTTP/1.1" 200 11746 "-" "snap/1.1.53 CFNetwork/758.5.3 Darwin/15.6.0" "-"
220.248.15.74 - - [2016-08-09T00:24:56+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=F59B7A3F03317289EFDC9648C4D507B0_motion_1470646030985_small.jpg HTTP/1.1" 200 12758 "-" "snap/1.1.53 CFNetwork/758.5.3 Darwin/15.6.0" "-"
220.248.15.74 - - [2016-08-09T00:24:57+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=F59B7A3F03317289EFDC9648C4D507B0_motion_1470646494666_small.jpg HTTP/1.1" 200 12942 "-" "snap/1.1.53 CFNetwork/758.5.3 Darwin/15.6.0" "-"
220.248.15.74 - - [2016-08-09T00:25:03+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=F59B7A3F03317289EFDC9648C4D507B0_motion_1470644654148_small.jpg HTTP/1.1" 200 12263 "-" "snap/1.1.53 CFNetwork/758.5.3 Darwin/15.6.0" "-"
220.248.15.74 - - [2016-08-09T00:25:07+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=F59B7A3F03317289EFDC9648C4D507B0_motion_1470644291204_small.jpg HTTP/1.1" 200 12690 "-" "snap/1.1.53 CFNetwork/758.5.3 Darwin/15.6.0" "-"
220.248.15.74 - - [2016-08-09T00:25:08+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=F59B7A3F03317289EFDC9648C4D507B0_motion_1470643977078_small.jpg HTTP/1.1" 200 12680 "-" "snap/1.1.53 CFNetwork/758.5.3 Darwin/15.6.0" "-"
```

## 用shell的方式处理日志并对ip字段排序
```shell
# awk '{ print $1 }' access-8000.log | sort -n  | uniq -c | sort -n -r | head -n 10
   1924 219.232.105.98
    437 219.232.105.104
    329 220.248.15.74
    297 54.222.138.168
    236 219.232.105.102
    159 49.95.188.36
    136 54.222.132.12
    116 54.222.133.100
     67 219.232.105.99
     43 101.81.225.57
```


## 单线程
```python
import sys

def main(logfile):
    ips = {}
    with open(logfile, 'r') as f:
        count = 1
        for line in f:
            ip = line.split()[0]
            if ip not in ips:
                ips[ip] = count
            else:
                ips[ip] = ips[ip] + 1

    return sorted(ips.items(), key=lambda x:x[1], reverse=True)

if __name__ == '__main__':
    print main(sys.argv[1])
```

## 多线程 
> hadoop中map/reduce分治的思想

> map的过程 将一个大的进行拆分成若干小份 分别计算.

> reduce过程 对每个小份的计算结果 进行合并

```python
#coding:utf-8

import time

fd = open('/root/access-8000.log', 'r')
fd.seek(0, 2)
max_size = fd.tell()

fd.seek(0, 0)
fd.tell()

ThreadNum = 8
offsize = int ( max_size / ThreadNum )
ranges = []
for x in xrange(ThreadNum):
    if x == ThreadNum -1:
        th = (x * offsize, max_size)
    else:
        th = (x * offsize, (x+1) * offsize)
    ranges.append(th)
    
print max_size
print ranges
print offsize
time.sleep(5)

# [(0, 13612), (13612, 27224), (27224, 40836), (40836, 54448), (54448, 68060), (68060, 81672), (81672, 95284), (95284, '')]
for ran in ranges:
    start, end = ran
    buf = end - start
    fd.seek(start, 0)
    data = fd.read(buf)

    print 'start %s, end %s' % (start, end)
    print data
    print '-'*70
    time.sleep(0.5)

fd.close()
```

```
#coding:utf-8

import re
import sys
import logging
import threading

class Thread(object):
    def __init__(self, log_file, ThreadNum):
        self.log_file = log_file        
        self.ThreadNum = ThreadNum
        self.fd = open(self.log_file, 'r') 
        self.results = []
        self.offsize = None

    def get_ranges(self):
        self.fd.seek(0, 2)
        max_size = self.fd.tell()

        offsize = int ( max_size / self.ThreadNum)
        self.offsize = offsize
        ranges = []
        for x in xrange(self.ThreadNum):
            if x == self.ThreadNum -1:
                th = (x * offsize, max_size)
            else:
                th = (x * offsize, (x+1) * offsize)
            ranges.append(th)
        logging.debug('ranges:%s' % ranges)
        return ranges

    def read_buf(self, start, buf):
        self.fd.seek(start, 0)
        data = self.fd.read(buf)
        match = re.match(r'^[\d.]{7,}', data)
        if not match:   # 如果不是以数字开头的 就排除这一行.
            lines = data.strip().split('\n')[1:]
        else:
            lines = data.split('\n')

        ips = {}
        count = 1
        for line in lines:
            if not line:
                continue
            ip = line.split()[0]
            if ip not in ips:
                ips[ip] = count
            else:
                ips[ip] = ips[ip] + 1
        logging.debug('ips:%s' % ips)
        self.results.append(ips)

    def sorted_for_dic(self, m={}):
        return sorted(m.items(), key=lambda x:x[1], reverse=True)

    def map_process(self):
        for ran in self.get_ranges():
            start, end = ran
            buf = end -start
            t = threading.Thread(target=self.read_buf, name='thread-%s' % ( int(start) / self.offsize + 1 ), args=(start, buf))
            t.start()
        t.join()
        self.fd.close()

    def reduce_process(self):
        m = {}
        for line in self.results:
            for k, v in line.items():
                if k not in m:
                    m[k] = v
                else:
                    m[k] = m[k] + v
        return m
    
    def process(self):
        logging.debug('execute map finish.')
        self.map_process()
        logging.debug('execute reduce finish.')
        m = self.reduce_process()
        logging.debug('sorted finish.')
        return self.sorted_for_dic(m)

if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(threadName)s %(filename)s line:%(lineno)d %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    t = Thread('access-8000.log', 8)
    print t.process()
```

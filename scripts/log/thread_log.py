#coding:utf-8

import re
import sys
import logging
import threading

'''
hadoop中map/reduce分治的思想.
map的过程 将一个大的进行拆分成若干小份 分别计算.
reduce过程 对每个小份的计算结果 进行合并.
'''

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
    t = Thread('access.log', 8)
    print t.process()

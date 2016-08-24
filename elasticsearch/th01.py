# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import time
import json
import redis
import logging

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, parallel_bulk

class elasctic(object):
    def __init__(self, host='127.0.0.1', port=9200, flush_size=2000):
        self.host = host
        self.port = port 
        self.conn = None
        self.flush_size = flush_size

    def connect(self):
        self.conn = Elasticsearch([
                        {'host' : self.host}, 
                        {'port' : self.port}
                        ])

    def bulkdata(self, data):
        self.connect()
        # bulk(client=self.conn, actions=data, stats_only=True)
        parallel_bulk(client=self.conn, actions=data, thread_count=4, chunk_size=500)


class Redis(object):
    def __init__(self, host='127.0.0.1', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.r = None
        self.es = elasctic()

    def connect(self):
        self.r = redis.Redis(host=self.host, port=self.port, db=self.db)

    def pop_from_redis(self, key):
        return self.r.lpop(key)

    def get_queue_length(self, key):
        return self.r.llen(key)

    def format_data(self, data):
        jsondata = json.loads(data)
        format_data = {
                "_index" : 'zhengys',
                "_type" : jsondata['type'],
                "timestamp" : jsondata['@timestamp'],
                "host" : jsondata['host'],
                "public_ip" : jsondata['public_ip'],
                "path" : jsondata['path'],
                "message" : jsondata['message']
                }
        return format_data

    def process(self, key):
        self.connect()
        
        cache = []
        interval = 5 

        while True:
            length = self.get_queue_length(key)
            if length == 0:
                logging.debug('key:%s, pop finish.' % self.key)
                time.sleep(interval)
            else:
                value_str = self.pop_from_redis(key)
                format_record = self.format_data(value_str)
                cache.append(format_record)

                if len(cache) == self.es.flush_size:
                    time.sleep(interval)
                    self.es.bulkdata(cache)
                    logging.debug('flush_size:%s, bulk data to es finish.' % self.es.flush_size)
                    cache = []
                    continue
                

def main():
    r = Redis(host='127.0.0.1', port=6380)
    r.process("logstash:redis")

if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(filename)s line:%(lineno)d %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    main()
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

msg = '''
219.232.105.97 - - [23/Aug/2016:08:20:31 +0000] "GET /bundles/node_modules/font-awesome/fonts/fontawesome-webfont.woff2 HTTP/1.1" 304 0 "http://52.38.135.142:8000/bundles/statusPage.style.css?v=9689" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
'''

bulk_data = []
for id in xrange(20000):
     bulk_data.append({"_index" : "sengled", "_type" : "nginx", "_id" : id, 'timestamp':datetime.now(), "doc" : msg})

client = Elasticsearch([{'host' : 'localhost'}, {'port' : 9200}])
bulk(client, bulk_data)
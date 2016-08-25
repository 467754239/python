# -*- coding: utf-8 -*-
from __future__ import unicode_literals

data = {u'_type': u'media', u'_index': u'zhengys', u'timestamp': u'2016-08-25T03:08:37.894Z', u'public_ip': u'52.39.240.118', u'host': u'ip-172-31-13-135', u'path': u'/var/log/sengled/media/StreamingServer.log', u'message': u'About to close UDP Socket'}

bulk_data = []
bulk_data.append(data)
print len(bulk_data)

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, parallel_bulk, streaming_bulk

esconn = Elasticsearch([{'host' : '127.0.0.1'}, {'port' : 9200}])
bulk(client=esconn, actions=bulk_data, stats_only=False)

streaming_bulk(client=esconn, actions=bulk_data)
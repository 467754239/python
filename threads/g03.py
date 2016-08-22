# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from gevent import monkey; monkey.patch_socket()
import gevent
import urllib2

def func(url):
    print "GET: %s" % url
    resp = urllib2.urlopen(url)
    data = resp.read()
    print "%d bytes received from %s." % (len(data), url)

gevent.joinall([
        gevent.spawn(func, 'http://www.baidu.com'),
        gevent.spawn(func, 'http://467754239.blog.51cto.com'),
        gevent.spawn(func, 'http://www.sina.com'),
    ])

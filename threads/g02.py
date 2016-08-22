# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from gevent import monkey; monkey.patch_socket()
import gevent

def func(n):
    for i in range(n):
        print gevent.getcurrent(), i
        gevent.sleep(0)

g1 = gevent.spawn(func, 5)
g2 = gevent.spawn(func, 5)
g3 = gevent.spawn(func, 5)

g1.join()
g2.join()
g3.join()
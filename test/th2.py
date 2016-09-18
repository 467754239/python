# -*- coding: utf-8 -*-
from __future__ import unicode_literals

oldlist = range(10)
del_items = [3, 5]

print [x for x in oldlist if x not in del_items ]

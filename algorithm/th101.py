# -*- coding: utf-8 -*-
from __future__ import unicode_literals

list = [1,2,3,2,12,3,1,3,21,2,2,3,4111,22,3333,444,111,4,5,777,65555,45,33,45]

max_val = list[0]

for x in list[1:]:
    if x > max_val:
        sec_val = max_val
        max_val = x
        
print "Max:%s, Sec:%s" % (max_val, sec_val)
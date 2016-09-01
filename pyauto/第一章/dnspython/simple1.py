# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import dns.resolver

domain = raw_input('please input a domain: ')

dm_iter = dns.resolver.query(domain)
for iter in dm_iter:
    print iter


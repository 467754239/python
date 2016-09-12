# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time
import json
import base64
import hashlib
import ConfigParser

def get_config(section):
    config_file = 'zhengys.conf'
    config = ConfigParser.ConfigParser()
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    service_conf = os.path.join(cur_dir, config_file)
    try:
        config.read(service_conf)
        return dict(config.items(section))
    except Exception as e:
        app.logger.error('-----get configurating failed, %s.-----' % e)
        return {}

def create_token(username, role, passport):
    cur_time = int(time.time())
    md5_token = hashlib.md5('%s%s%s' % (username, cur_time, passport)).hexdigest()
    return base64.b64encode('%s|%s|%s|%s' % (username, cur_time, role, md5_token)).strip()

def valid_token(token, passport):
    # 'admin|1473676673|admin|aa0dc873a1a2d15757a765e4f7b50426'
    session_ttl = int(2 * 60 * 60)   # 2h
    cur_time = int(time.time())
    decode_token = base64.b64decode(token)      # token解码.
    token_args = decode_token.split('|')
    if len(token_args) != 4:
        app.logger.error('token args num error.')
        return json.dumps({'code' : 1, 'errmsg' : 'args num error.'})

    if cur_time > int(token_args[1]) + session_ttl:   
        app.logger.error('token session expire.')
        return json.dumps({'code' : 1, 'errmsg' : 'session expire.'})

    return json.dumps({'code' : 0, 'username' : token_args[0], 'role' : token_args[2]})


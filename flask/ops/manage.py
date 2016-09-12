# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import logging
from logging.handlers import RotatingFileHandler

from app import app
from dbMysql import dbmysql
from utils import get_config as config

app.config.update(
    DEBUG = True,                                               # 是否开启debug调试模式.
    passport = '123456',                                        # 密令，通行证.
    SECRET_KEY = '\x90\x13\xfd\r\x1c\x84\x03;Z\xea',            # 秘钥(os.urandom(24)[:15]).
    mysqlconn = dbmysql(**config('mysql'))
)

if __name__ == '__main__':
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s- %(levelname)s - %(message)s')
    handler = RotatingFileHandler('/var/log/flask.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    app.run(host='0.0.0.0', port=5000) 

#coding:utf-8

import os
import logging
import logging.config
import ConfigParser

global logger

'''日志配置'''
def logging_conf():
    global logger
    logging.config.fileConfig('./conf/logging.conf')
    logger = logging.getLogger('general')

def get_config(section):
    config = ConfigParser.ConfigParser()
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    service_conf = os.path.join(cur_dir, './conf/config.ini')
    try:
        config.read(service_conf)
        conf_items = dict(config.items(section))
    except Exception as e:
        print 'load config file error, %s', e
        conf_items = {}
    return conf_items

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import ConfigParser

def config(section):
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
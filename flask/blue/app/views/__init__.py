# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint

# Blueprint(self, name, import_name, static_folder=None, static_url_path=None, template_folder=None, url_prefix=None, subdomain=None, url_defaults=None)
# 这个构造函数有两个必须指定的参数：蓝本的名字和蓝本所在的包或模块.
asset = Blueprint('asset', __name__)

from . import login 
from . import logout

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Flask
from .views import asset

app = Flask(__name__)

app.register_blueprint(asset)

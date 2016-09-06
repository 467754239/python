# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.script import Manager
from flask import Flask

app = Flask(__name__)
manager = Manager(app)

@manager.command
# @app.route('/')
def hello(username):
    return 'hello %s!' % username

if __name__ == '__main__':
    # python run2.py hello zhengysa
    manager.run()
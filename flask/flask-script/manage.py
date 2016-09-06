# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.script import Manager
from flask import Flask

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
    return 'hello world!'


if __name__ == '__main__':
    # python run.py runserver -h 0.0.0.0 -p 5000 -r
    manager.run()
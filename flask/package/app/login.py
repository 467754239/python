# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import app

@app.route('/login', methods=['POST'])
def manage_login():
    return 'manage login.', 200
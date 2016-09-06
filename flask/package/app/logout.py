# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import app

@app.route('/logout', methods=['POST'])
def manage_logout():
    return 'manage logout.', 200
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from . import app
from flask import Flask, request, session, render_template, redirect, url_for
from utils import config
from dbMysql import dbmysql

@app.route('/')
@app.route('/index', methods=['GET'])
def manage_index():
    if not session.get('username'):
        return redirect(url_for('login'))
    return render_template('index.html', info=session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        # { k:v[0] for k, v in dict(request.form).items() }
        username = request.form.get('username')
        password = request.form.get('password')
        app.logger.debug('username:%s, password:%s' % (username, password))
        query_result = app.config['mysqlconn'].get_one_result(table_name='users', fields=['password', 'role'], where={'name':username})
        app.logger.debug('query result:%s.' % str(query_result))

        password_db = query_result.get('password', None)
        role_name = query_result.get('role')

        if not password_db:
            return json.dumps({'code' : 1, 'errmsg' : 'user is not exists.'})
        elif password != password_db:
            return json.dumps({'code' : 1, 'errmsg' : 'password error.'})

        session['username'] = username
        session['role'] = role_name
        return json.dumps({'code' : 0, 'result' : 'login sucessful.'})

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if session.get('username'):
        session.pop('role', None)
        session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/userlist', methods=['GET', 'POST'])
def userlist():
    pass
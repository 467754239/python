# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from . import app
from flask import Flask, request, session, render_template, redirect, url_for
from dbMysql import dbmysql

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
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
        query_result = app.config['mysqlconn'].get_one_result(table_name='user', fields=['password', 'role'], where={'name' : username})
        app.logger.debug('query result:%s.' % str(query_result))

        password_db = query_result.get('password', None)
        role_name = query_result.get('role')

        if not password_db:
            return json.dumps({'code' : 1, 'errmsg' : 'user not exists.'})
        elif password != password_db:
            return json.dumps({'code' : 1, 'errmsg' : 'password error.'})

        session['username'] = username
        session['role'] = role_name
        return json.dumps({'code' : 0, 'result' : 'login sucessful.'})

@app.route('/logout', methods=['GET'])
def logout():
    if session.get('username'):
        session.pop('role', None)
        session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if not session.get('username'):
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('add.html', info=session)
    elif request.method == 'POST':
        add_userinfo = { k: v[0] for k, v in dict(request.form).items() }
        app.logger.debug('add_user; data:%s.' % json.dumps(add_userinfo))
        query_result = app.config['mysqlconn'].get_one_result(table_name='user', fields=['name'], where={'name' : add_userinfo['name']})
        app.logger.debug('add_user; query_result:%s.' % json.dumps(query_result))
        if query_result:
            return json.dumps({'code' : 1, 'errmsg' : 'username is exists.'})
        else:
            code = app.config['mysqlconn'].execute_insert_sql(table_name='user', data=add_userinfo)
            if code != 0:
                return json.dumps({'code' : 0, 'result' : 'add user sucessful.'})
            else:
                return json.dumps({'code' : 1, 'errmsg' : 'add user to db failed.'})

@app.route('/delete', methods=['GET', 'POST'])
def delete_user():
    if not session.get('username'):
        return redirect(url_for('login'))
    uid = request.args.get('id')
    app.logger.debug('delete user, uid:%s.' % uid)
    code = app.config['mysqlconn'].execute_delete_sql(table_name='user', where={'id' : uid})
    if code == 1:
        app.logger.debug('delete user sucessful, uid:%s' % uid)
        return json.dumps({'code':0, 'result':'delete user sucessful'})
    else:
        app.loger.warnning('delete user failed, uid:%s' % uid)
        return json.dumps({'code':1, 'result':'delete user failed'})

@app.route('/userlist', methods=['GET', 'POST'])
def userlist():
    if not session.get('username'):
        return redirect(url_for('/login'))

    fields = ["id", "name", "name_cn", "mobile", "email", "role", "status"]
    query_result = app.config['mysqlconn'].get_all_results(table_name='user', fields=fields)
    app.logger.debug('userlist; query result:%s.' % str(query_result))
    return render_template('userlist.html', users=query_result, info=session)

@app.route('/server', methods=['GET', 'POST'])
def server():
    if not session.get('username'):
        return redirect(url_for('/login'))

    fields = ['hostname', 'public_ip', 'private_ip', 'memtotal', 'disk_size', 'logic_cpu_num', 'swaptotal', 'os_kernel', 'update_datetime', 'model_name', 'serial_number', 'os_type', 'product_name', 'manufacturer']
    query_result = app.config['mysqlconn'].get_all_results(table_name='server', fields=fields)
    return render_template('server_list_os.html', data=query_result, info=session)

@app.route('/hostinfo', methods=['GET', 'POST'])
def hostinfo():
    if not session.get('username'):
        return redirect(url_for('/login'))
        
    if request.method == 'POST':
        data = request.json
        hostname_list = app.config['mysqlconn'].get_one_result(table_name='server', fields=['hostname'], where={'hostname' : data.get('hostname')})
        app.logger.debug('hostname_list:%s.' % json.dumps(hostname_list))
        if not hostname_list:
            app.config['mysqlconn'].execute_insert_sql(table_name='server', data=data)
        else:
            fields = ['public_ip', 'private_ip', 'memtotal', 'disk_size', 'logic_cpu_num', 'swaptotal', 'os_kernel', 'update_datetime', 'model_name', 'serial_number', 'os_type', 'product_name', 'manufacturer']
            app.config['mysqlconn'].execute_update_sql(table_name='server', data=data, fields=fields, where={'hostname' : hostname_list['hostname']})
    return '', 200
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import json
import hashlib
from . import app
from flask import Flask, request, session, render_template, redirect, url_for
from utils import create_token, valid_token

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    if not session.get('username'):
        return redirect(url_for('login'))
    return render_template('index.html', info=session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # { k:v[0] for k, v in dict(request.form).items() }
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            print 2
            return json.dumps({'code' : 1, 'errmsg' : 'your must input login username and password.'})

        query_result = app.config['mysqlconn'].get_one_result(table_name='user', fields=['password', 'role'], where={'name':username})
        if not query_result:
            return json.dumps({'code' : 1, 'errmsg' : 'user not exists.'})

        if query_result.get('password') != hashlib.md5(password).hexdigest():
            return json.dumps({'code' : 1, 'errmsg' : 'password error.'})
        else:
            data = {'last_login_time' : time.strftime('%Y-%m-%d %H:%M:%S')}
            app.config['mysqlconn'].execute_update_sql(table_name='user', data=data, where={'name' : username})

            role = query_result.get('role')
            token = create_token(username, role, app.config['passport'])

            decode_token_result = valid_token(token, app.config['passport'])
            session['token'] = token
            session['username'] = username
            return json.dumps({'code' : 0, 'result' : 'login sucessful.'})
    return render_template('login.html')

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

@app.route('/update_msg', methods=['GET'])
def update_msg():
    name = request.args.get('name')
    fields = ['id','name','name_cn','password','email','mobile','role','status']
    query_result = app.config['mysqlconn'].get_one_result(table_name='user', fields=fields, where={'name' : name})
    if session.get('role') == 'admin':
        return json.dumps({'code' : 0, 'result' : query_result})
    else:
        return json.dumps({'code' : 2, 'result' : query_result})

@app.route('/update', methods=['GET','POST'])
def update():
    if not session.get('username'):
        return redirect(url_for('login'))

    data = dict((k,v[0]) for k, v in dict(request.form).items())
    name = data.get('name')
    app.config['mysqlconn'].execute_update_sql(table_name='user', data=data, where={'name' : name})
    return json.dumps({'code' : 0, 'result' : 'update completed.'})

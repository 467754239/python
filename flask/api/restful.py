# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    if request.method == 'GET':
        # curl 'localhost:5000/?username=zhengys&password=123456'
        username = request.args.get('username')
        password = request.args.get('password')
        return 'action:get, username:%s, password:%s.' % (username, password)

    elif request.method == 'POST':
        '''
        # curl -X POST 'localhost:5000/' -d 'username=zhengys&password=123456'
        # 这种用requests.post会出错.

        # curl -H "Content-Type: application/json" -X POST  -d '{"username":"zhengys", "password":"123456"}'  http://127.0.0.1:5000
        username = request.form.get('username')
        password = request.form.get('password')
        return 'action:post, username:%s, password:%s.' % (username, password)
        '''

        '''
        print type(request.data), request.data
        alldata_string = request.data
        data_dict = json.loads(alldata_string)
        username = data_dict.get('username')
        password = data_dict.get('password')
        return 'action:post, username:%s, password:%s.' % (username, password)
        '''

        '''
        print type(request.json), request.json
        data_dict = request.json
        username = data_dict.get('username')
        password = data_dict.get('password')
        return 'action:post, username:%s, password:%s.' % (username, password)
        '''

        print type(request.get_json()), request.get_json()
        data_dict = request.get_json()
        username = data_dict.get('username')
        password = data_dict.get('password')
        return 'action:post, username:%s, password:%s.' % (username, password)

    elif request.method == 'PUT':
        pass

    elif request.method == 'DELETE':
        pass

@app.route('/<string:username>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manager_username(username):
    if request.method == 'GET':
        # curl -X GET 'localhost:5000/zhengys?password=123456'
        password = request.args.get('password')

    elif request.method == 'POST':
        # curl -X POST 'localhost:5000/zhengys' -d 'password=123456'
        password = request.form.get('password')

    elif request.method == 'PUT':
        # curl -H "Content-Type: application/json" -X PUT  -d '{"password":"123456"}'  http://127.0.0.1:5000/zhengys
        password = request.json.get('password')

    elif request.method == 'DELETE':
        pass

    action = request.method
    return 'action:%s, username:%s, password:%s.' % (action.lower(), username, password)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
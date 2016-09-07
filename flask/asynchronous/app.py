# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from flask import Flask, request
from gevent import monkey
from gevent.pywsgi import WSGIServer

from geventwebsocket.handler import WebSocketHandler 

monkey.patch_all()

app = Flask(__name__)

app.config.update(
    DEBUG=True
)

@app.route('/asyn/1/', methods=['GET'])
def test_asyn_one():
    if request.method == 'GET':
        time.sleep(10)
        return 'hello asyn'


@app.route('/test/', methods=['GET'])
def test():
    return 'hello test'


if __name__ == "__main__":
    # app.run()
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()



    '''
    http://blog.csdn.net/danny_amos/article/details/50859383
    '''
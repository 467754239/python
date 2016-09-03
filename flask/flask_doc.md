# Flask #

A Minimal Application
```python
#!/usr/bin/env python
#coding:utf-8

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
```

支持post、get提交
> @app.route('/', methods=['GET', 'POST'])

多个url
> @app.route('/')  
> @app.route('/index')

不管post、get使用统一的接收
> from flask import request
> args = request.args if request.method == 'GET' else request.form
> a = args.get('a', 'default')

```
from flask import request
if request.method == 'GET':
    args = request.args
else:
    args = request.form
a = args.get('a', 'default')
```

处理json请求
request的header中
> header = "Content-Type": "application/json"

处理时
> data = request.get_json(silent=False)

使用url参数
```
@app.route('/query/<qid>/')
def query(qid):
    pass
```

在request开始结束dosomething
```
from flask import g
 
app = .....
 
@app.before_request
def before_request():
    g.session = create_session()
 
@app.teardown_request
def teardown_request(exception):
    g.session.close()
```

注册Jinja2模板中使用的过滤器
```
@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]

#或者

def reverse_filter(s):
    return s[::-1]
app.jinja_env.filters['reverse'] = reverse_filter

#或者

def a():...
def b():...
 
FIL = {'a': a, 'b':b}
app.jinja_env.filters.update(FIL)
```


注册Jinja2模板中使用的全局变量
```
JINJA2_GLOBALS = {'MEDIA_PREFIX': '/media/'}
app.jinja_env.globals.update(JINJA2_GLOBALS)
```

定义应用使用的template和static目录
```
app = Flask(__name__, 
            template_folder=settings.TEMPLATE_FOLDER, static_folder=settings.STATIC_PATH
            )

```

使用Blueprint
```

from flask import Blueprint
bp_test = Blueprint('test', __name__)
#bp_test = Blueprint('test', __name__, url_prefix='/abc')
 
@bp_test.route('/')
 
--------
from xxx import bp_test
 
app = Flask(__name__)
app.register_blueprint(bp_test)
```

实例:
```
bp_video = Blueprint('video', __name__, url_prefix='/kw_news/video')
@bp_video.route('/search/category/', methods=['POST', 'GET'])
#注意这种情况下Blueprint中url_prefix不能以 '/' 结尾, 否则404
```

使用session
包装cookie实现的，没有session id
```
app.secret_key = 'PS#yio`%_!((f_or(%)))s'
 
# 然后
from flask import session
 
session['somekey'] = 1
session.pop('logged_in', None)
 
session.clear()
 
#过期时间,通过cookie实现的
from datetime import timedelta
session.permanent = True
app.permanent_session_lifetime = timedelta(minutes=5)

反向路由

from flask import url_for, render_template
 
@app.route("/")
def home():
    login_uri = url_for("login", next=url_for("home"))
    return render_template("home.html", **locals())
```


上传文件
```
<form action="/image/upload/" method="post" enctype="multipart/form-data">
<input type="file" name="upload" />
```

接收
```
f = request.files.get('upload')
img_data = f.read()
```

直接返回某个文件
```
return send_file(settings.TEMPLATE_FOLDER + 'tweet/tweet_list.html')
```

请求重定向
文档（http://flask.pocoo.org/docs/api/#flask.redirect）
flask.redirect(location, code=302) the redirect status code. defaults to 302.Supported codes are 301, 302, 303, 305, and 307. 300 is not supported.

```
@app.route('/')
def hello():
    return redirect(url_for('foo'))
 
@app.route('/foo')
def foo():
    return'Hello Foo!'
```

获取用户真实ip

从request.headers获取
```
real_ip = request.headers.get('X-Real-Ip', request.remote_addr)
```

或者, 使用werkzeug的middleware 文档
```
from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
```

return json & jsonp
```
import json
from flask import jsonify, Response, json
 
data = [] # or others
return jsonify(ok=True, data=data)
 
jsonp_callback =  request.args.get('callback', '')
if jsonp_callback:
    return Response(
            "%s(%s);" % (jsonp_callback, json.dumps({'ok': True, 'data':data})),
            mimetype="text/javascript"
            )
return ok_jsonify(data)
```

配置读取方法
```
# create our little application :)
app = Flask(__name__)
 
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='/tmp/flaskr.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
 
------------------
# configuration
DATABASE = '/tmp/minitwit.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'
 
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)
```

几个不常用的方法
```
from flask import abort, flash
 
abort
if not session.get('logged_in'):
    abort(401)
 
flash
flash('New entry was successfully posted')
```

异步调用
想在flask的一个请求中处理异步, 除了使用消息系统, 可以用简单的线程处理
```
from threading import Thread
 
def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
 
@async
def dosomething(call_args):
    print call_args
 
in a request handler, call `dosomething`
```

error handler
```
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
 
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
```

项目配置

```
1.直接
app.config['HOST']='xxx.a.com'
print app.config.get('HOST')

2.环境变量
export MyAppConfig=/path/to/settings.cfg
app.config.from_envvar('MyAppConfig')

3.对象
class Config(object):
     DEBUG = False
     TESTING = False
     DATABASE_URI = 'sqlite://:memory:'
 
 class ProductionConfig(Config):
     DATABASE_URI = 'mysql://user@localhost/foo'
 
 app.config.from_object(ProductionConfig)
 print app.config.get('DATABASE_URI') # mysql://user@localhost/foo

 4.文件
 # default_config.py
HOST = 'localhost'
PORT = 5000
DEBUG = True
 
app.config.from_pyfile('default_config.py')
```

EG. 一个create_app方法
```
from flask import Flask, g
 
def create_app(debug=settings.DEBUG):
    app = Flask(__name__,
                template_folder=settings.TEMPLATE_FOLDER,
                static_folder=settings.STATIC_FOLDER)
 
    app.register_blueprint(bp_test)
 
    app.jinja_env.globals.update(JINJA2_GLOBALS)
    app.jinja_env.filters.update(JINJA2_FILTERS)
 
    app.secret_key = 'PO+_)(*&678OUIJKKO#%_!(((%)))'
 
    @app.before_request
    def before_request():
        g.xxx = ...    #do some thing
 
    @app.teardown_request
    def teardown_request(exception):
        g.xxx = ...    #do some thing
 
    return app
 
app = create_app(settings.DEBUG)
host=settings.SERVER_IP
port=settings.SERVER_PORT
app.run(host=host, port=port)
```

## 参考资料 ##
[Welcome to Flask](http://flask.pocoo.org/docs/0.10/)
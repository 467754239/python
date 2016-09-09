# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

from flask import Flask, redirect, render_template, request, session, url_for, flash, send_from_directory
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, HiddenField, SubmitField
from wtforms.validators import Required

from werkzeug import secure_filename


app = Flask(__name__)

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

books = []

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config.update(
    DEBUG = True,                                   # 是否开启debug调试模式.
    SECRET_KEY = 'hard to guess string',            # 秘钥(os.urandom(24)).
    UPLOAD_FOLDER = '/tmp/uploads',                 # 上传文件到服务器的目录.
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024,          # 16M
)


class NameForm(Form):
    username = StringField('What is your username?', validators=[Required()])
    submit = SubmitField('submit')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if session.get('username'):
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            return redirect(url_for('login'))
    return render_template('login.html', username=username)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        pass
    else:
        pass

@app.route('/', methods=['GET', 'POST'])
def index():
    app.logger.debug('session:%s.' % session)
    form = NameForm()
    if form.validate_on_submit():       # 表单中的数据是否被所有的验证函数接受，接受return True，否则return False.
        old_username = session.get('username')
        if old_username is None or old_username != form.username.data:
            flash('Look like you have changed your name!')
        session['username'] = form.username.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, username=session.get('username'))

'''
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    # print dir(form)
    # print form.validate_on_submit()
    if form.validate_on_submit():       # 表单中的数据是否被所有的验证函数接受，接受return True，否则return False.
        session['username'] = form.username.data
        # return redirect('/')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, username=session.get('username'))
'''

'''
@app.route('/', methods=['GET', 'POST'])
def index():
    username = None
    form = NameForm()
    if form.validate_on_submit():
        username = form.username.data
        form.username.data = ''
    return render_template('index.html', form=form, username=username)
'''

'''
@app.route('/')
def index():
    # return '<h1>Hello World!</h1>'
    # return render_template('index.html')
    return render_template('index.html', current_time=datetime.utcnow())
'''

@app.route('/user/<name>')
def user(name):
    # return '<h1>Hello, %s!</h1>' % name
    return render_template('user.html', name=name)

@app.route('/usern/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user.name

@app.route('/baidu')
def skip_baidu():
    return redirect('http://www.baidu.com')

@app.route('/form')
def manage_form():
    username = request.args.get('username')
    password = request.args.get('password')
    return render_template('form.html', username=username, password=password)

@app.route('/program_language/<program_language>')
def manage_username(program_language):
    global books
    books.append(program_language)
    books = list(set(books))
    return render_template('books.html', books=books)

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            app.logger.debug('upload file, file:%s.' % filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('upload_file'))
            return redirect(url_for('uploaded_file', filename=filename))
        else:
            app.logger.warning('file:%s not allow upload.' % file.filename)
            
    return render_template('upload_file.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

class load_user(object):
    def __init__(self, id):
        self.id = id
        self.name = self.get_user()

    def get_user(self):
        if int(self.id) == 0:
            return 'alex'
        else:
            return 'auxten'

def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        return True
    return False


if __name__ == '__main__':
    # app.run(debug=True)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s- %(levelname)s - %(message)s')
    handler = RotatingFileHandler('/var/log/flask.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    manager.run()

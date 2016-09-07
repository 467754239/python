# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from flask import Flask, redirect, render_template, request
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment


app = Flask(__name__)   

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

books = []

@app.route('/')
def index():
    # return '<h1>Hello World!</h1>'
    # return render_template('index.html')
    return render_template('index.html', current_time=datetime.utcnow())

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

if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()

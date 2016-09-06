from . import main
from flask import render_template

@main.route('/', methods=['GET', 'POST'])
def manage_index():
    return render_template('index.html')

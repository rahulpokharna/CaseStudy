# this is just a test file sibi made to learn how stuff works. were not actualy using this for anything.
from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html',name='Sibi')

@app.route('/hello/<username>/')
def hello(username):
    return 'Hello %s' % username


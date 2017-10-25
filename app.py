from flask import Flask, render_template, request, redirect
from login import LoginForm
app = Flask(__name__)

@app.route('/')
def index():
     form = LoginForm(request.form)
     return render_template('index.html', form = form)

@app.route('/kian')
def kian():
	return render_template('kianindex.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    print('Email: %s' % request.form['email'])
    print('Password: %s' % request.form['password'])

    print('REQUEST: %s' % request.form)
    if request.method == 'POST' and form.validate():
        print('REQUEST: %s' % request.data)
        if str(request.form['email']) == 'email' and str(request.form['password']) == 'password':
            return redirect('/kian')
        else:
            print(str(request.form['email']))
            print(str(request.form['password']))

@app.route('/home')
def home():
    return render_template('home.html')


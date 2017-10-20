from flask import Flask, render_template, request, redirect
from login import LoginForm
app = Flask(__name__)

@app.route('/')
def index():
     form = LoginForm(request.form)
     return render_template('index.html', form = form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    print('REQUEST: %s' % request.data)
    if request.method == 'POST' and form.validate():
        print('REQUEST: %s' % request.data)
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html')


from flask import Flask, render_template, request, redirect, make_response, jsonify
from login import LoginForm
from dbRequests import *
app = Flask(__name__)

@app.route('/')
def index():
     form = LoginForm(request.form)
     return render_template('index.html', form = form)

@app.route('/kian')
def kian():
	return render_template('calendarChild.html')

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
            return redirect('/')
# This method is to either get event(s) or to create a new one.
# for get request request with userId or eventId as url parameters (put it after the url like:
# localhost://5000/requests/events?userID=1
# for post request put the event object as the form. so form.title is the event's title, etc.
@app.route('/request/events', methods=['GET','POST','DELETE'])
def requestEvent():
    #request with userID or eventID given as url parameters. If eventId is not given, this will return all events for this user.
    if request.method == 'GET':
        userID = request.args.get('userID')
        eventID = request.args.get('eventID')
        if eventID == None:
            try:
                res = jsonify(getUserEvents(userID))
            except TypeError as e:
                res = 'couldnt jsonify the event'
                return res
        else:
            try:
                res =  jsonify(getEvent(eventID))
            except TypeError as e:
                res = 'couldnt jsonify the event'
                return res
        return res
    if request.method == 'POST':
        form = request.form
        #make a dictionary that can be put into the db. https://fullcalendar.io/docs/event_data/Event_Object/
        eventDict = {
            'Title' : form['title'],
            'Start' : form['start'],
            'End' : form['end']
        }
        return addNewEvent(eventDict)
    if request.method == 'DELETE':
        eventID = request.args.get('eventID')
        deleteEvent(eventID)

@app.route('/request/studyplan',methods=['POST'])
def setStudyPlan():
    if request.method == 'POST':
        form = request.form
        id = form['id']
        studyplan = form['studyplan']
        return editStudyEvent(id, studyplan)
        

        

    


@app.route('/home')
def home():
    return render_template('home.html')


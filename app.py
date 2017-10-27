from flask import Flask, render_template, request, redirect, make_response, jsonify
from login import LoginForm
from dbRequests import *
app = Flask(__name__)

@app.route('/')
def index():
     form = LoginForm(request.form)
     return render_template('index.html', form = form)

@app.route('/calendar')
def kian():
    return render_template('calendarChild.html')

@app.route('/study')
def study():
    return render_template('studyChild.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    # print('Email: %s' % request.form['email'])
    # print('Password: %s' % request.form['password'])

    # print('REQUEST: %s' % request.form)
    if request.method == 'POST' and form.validate():
        # print('REQUEST: %s' % request.data)
        if str(request.form['email']) == 'email' and str(request.form['password']) == 'password':
            return redirect('/kian')
        else:
            # print(str(request.form['email']))
            # print(str(request.form['password']))
            return redirect('/')
# This method is to either get event(s) or to create a new one or edit them.
# for get request request with userId or eventId as url parameters (put it after the url like:
# localhost://5000/requests/events?userID=1
# for post request put the event object as the form. so form.title is the event's title, etc.
@app.route('/request/events', methods=['GET','POST','DELETE'])
def requestEvent():
    #request with userID or eventID given as url parameters. If eventId is not given, this will return all events for this user.
    if request.method == 'GET':
        delete = request.args.get('delete')
        if delete == 'true':
            #delete this event.
            eventID = request.args.get('eventID')
            return deleteEvent(eventID)
        else:
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
        if 'id' in form:
            #trying to edit an event, not add one.
            eventDict ={
                'EventID' : form['id'],
                'Title' : form['title'],
                'Start' : form['start'],
                'End' : form['end']
            }
            return editEvent(form['id'],eventDict)
        else:
            #adding an event, not editting one.
            eventDict = {
                'Title' : form['title'],
                'Start' : form['start'],
                'End' : form['end']
            }
            return addNewEvent(eventDict)
            
    
     
#request to get or set a study plan for a given event Put eventID in the URL. 
@app.route('/request/studyplan',methods=['GET','POST'])
def setStudyPlan():
    if request.method == 'POST':
        form = request.form
        id = form['eventID']
        studyplan = form['studyplan']
        return editStudyEvent(id, studyplan)
    if request.method == 'GET':
        id = request.args.get('eventID')
        return viewStudyPlan('eventID')


@app.route('/home')
def home():
    return render_template('home.html')


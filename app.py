from flask import Flask, render_template, request, redirect, make_response, jsonify, session, flash
from login import LoginForm
from dbRequests import *
from requestHelpers import *
import os
app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/')
def index():
    if validateSession():
        return redirect('/calendar')
    else:
        session['logged_in'] = False
        return redirect('/welcome')

@app.route('/calendar')
def calendar():
    if validateSession():
        return render_template('calendarChild.html')
    else:
        return redirect('/welcome')

@app.route('/study')
def study():
    return render_template('studyChild.html')

# @app.route('/login', methods=['GET','POST'])
# def login():
#     form = LoginForm(request.form)
#     # print('Email: %s' % request.form['email'])
#     # print('Password: %s' % request.form['password'])
#
#     # print('REQUEST: %s' % request.form)
#     if request.method == 'POST' and form.validate():
#         # print('REQUEST: %s' % request.data)
#         if str(request.form['email']) == 'email' and str(request.form['password']) == 'password':
#             return redirect('/calendar')
#         else:
#             # print(str(request.form['email']))
#             # print(str(request.form['password']))
#             return redirect('/')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['POST'])
def login():
    userId = checkLogin(request.form['email'], request.form['password'])
    if userId != -1:
        session['logged_in'] = True
        session['email'] = request.form['email']
        session['userId'] = userId
        return redirect('/calendar')
    else:
        flash('Username or password is incorrect')
        return redirect('/welcome')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect('/welcome')

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
            print(form)
            return addEventRequest(form)



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

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if getUser(request.form['email']) is None:
        addNewUser(request.form)
        return redirect('/welcome')
    else:
        flash('email already taken')
        return redirect('/register')


# @app.route('/home')
# def home():
#     return render_template('home.html')

def validateSession():
    if 'logged_in' in session and session['logged_in'] == True and session['email'] != None:
        return True
    else:
        session['logged_in'] = False
        return False


if __name__ == "__main__":
    app.run()
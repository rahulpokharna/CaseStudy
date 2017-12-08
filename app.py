from flask import Flask, render_template, request, redirect, make_response, jsonify, session, flash
from login import LoginForm
from dbRequests import *
from requestHelpers import *
import google_stuff.google_stuff as google_stuff
import os
import pickle

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
    if validateSession():
        return render_template('studyChild.html')
    else:
        return redirect('/welcome')

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

@app.route('/studyDashboard')
def studyDashboard():
    if validateSession():
        return render_template('studyDashboard.html')
    else:
        return redirect('/welcome')

@app.route('/login', methods=['POST'])
def login():
    userId = checkLogin(request.form['email'], hashString(request.form['password']))
    if userId != -1:
        session['logged_in'] = True
        session['email'] = request.form['email']
        session['userId'] = userId
        user = makeUserDict(getUser(session['email']))
        if 'GoogleID' in user:
            googleID = user['GoogleID']
            if googleID != '-1':
                session['image'] = google_stuff.profileImage(googleID)
            else:
                session['image'] = None

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
@app.route('/request/events', methods=['GET','POST'])
def requestEvent():
    #request with userID or eventID given as url parameters. If eventId is not given, this will return all events for this user.
    print(request.method)
    if request.method == 'GET':
        delete = request.args.get('delete')
        if delete == 'true':
            return deleteEvent(request.args.get('eventID')  )
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
        if 'EventID' in form:
            print('eddddditing')
            return editEventRequest(form)
        else:
            #adding an event, not editting one.
            print('addding')
            return addEventRequest(form)



#request to get or set a study plan for a given event Put eventID in the URL.
@app.route('/request/studyplan',methods=['GET','POST'])
def setStudyPlan():
    if request.method == 'POST':
        form = request.form
        id = form['eventID']
        studyplan = form['studyplan']
        editStudyEvent(id, studyplan)
        return redirect('/calendar')
    if request.method == 'GET':
        id = request.args.get('eventID')
        return viewStudyPlan('eventID')

@app.route('/request/getUserPrograms', methods=['GET'])
def reqeuest_getUserPrograms():
    userID = request.args.get('userID')
    return jsonify(getUserPrograms(userID))

@app.route('/request/getGroupedUserEvents', methods=['GET'])
def reqeuest_getGroupedUserEvents():
    userID = request.args.get('userID')
    return jsonify(getGroupedUserEvents(userID))

@app.route('/request/getProgramEvents', methods=['GET'])
def request_getProgramEvents():
    userID = request.args.get('userID')
    programID = request.args.get('programID')
    return jsonify(getProgramEvents(userID, programID))

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

@app.route('/add_google')
def add_google():
    flow = google_stuff.get_flow()
    session['flow'] = pickle.dumps(flow)
    return redirect(google_stuff.get_step1(flow))

@app.route('/google_auth_code')
def google_auth_code():
    code = request.args.get('code')
    if not code:
        flash('unsuccessful adding google')
        return redirect('/calendar')

    google_stuff.set_credentials(code, session['userId'],pickle.loads(session['flow']))
    flash('successfully added google account')
    return redirect('/calendar')
# @app.route('/home')
# def home():
#     return render_template('home.html')

@app.route('/sync_google')
def sync_google_events():
    user = makeUserDict(getUser(session['email']))
    googleID = user['GoogleID']
    if googleID and googleID != -1:
        deleteGoogleEvents(session['userId'])
        num_events = google_stuff.add_events(googleID, session['userId'])
        flash('added {} events from google'.format(num_events))
        return redirect('/calendar')
    else:
        flash('no associated google account')
        return redirect('/calendar')

@app.route('/study_dashboard')
def study_dashboard():
    return render_template('studyDashboard.html')




def validateSession():
    if 'logged_in' in session and session['logged_in'] == True and session['email'] != None:
        return True
    else:
        session['logged_in'] = False
        return False


@app.route('/request/studyevents', methods=['GET','POST'])
def requestStudyEvent():
    #request with userID or eventID given as url parameters. If eventId is not given, this will return all events for this user.
    delete = request.args.get('delete')
    if delete == 'true':
        return deleteEvent(request.args.get('eventID')  )
    else:
        userID = request.args.get('userID')
        try:
            res = jsonify(getStudyEvents(userID))
        except TypeError as e:
            res = 'couldnt jsonify the event'
            return res
        return res


if __name__ == "__main__":
    app.run()


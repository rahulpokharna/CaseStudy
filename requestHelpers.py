from dbRequests import *
from flask import redirect
import hashlib

def addEventRequest(form):
    # :EventID, :UserID, :Start, :End, :Description, :ImportanceRanking, :Title, :ProgramID, :EventType, :StudyPlan, :StudyType
    # eventDict = {
    #     'Title': form['title'],
    #     'Start': form['start'],
    #     'End': form['end']
    # }
    #add :00 for the seconds
    form = form.to_dict()
    form['Start'] = '{}:00'.format(form['Start'])
    form['End'] = '{}:00'.format(form['End'])
    addNewEvent(form)
    return redirect('/calendar')

def editEventRequest(form):
    # trying to edit an event, not add one.
    # add :00 for the seconds
    form = form.to_dict()
    print(form['EventID'])
    form['Start'] = '{}'.format(form['Start'])
    form['End'] = '{}'.format(form['End'])
    editEvent(form['EventID'], form)
    return redirect('/calendar')
def hashString(string):
    m = hashlib.sha256()
    m.update(string.encode('utf-8'))
    return m.digest()

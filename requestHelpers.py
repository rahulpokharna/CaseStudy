from dbRequests import *
from flask import redirect
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
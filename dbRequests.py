import sqlite3
from sqlite3 import Error
import json

#Name/path of the database
DATABASE = 'test.db'
# Helper variable for events
defaultEvent = {'EventID': -1, 'UserID': 1, 'Start': '2017-10-26T18:53:08Z', 'End': '2017-10-26T19:53:08Z', 'Description': 'An Event', 'ImportanceRanking': 1, 'Title': 'Default Event', 'ProgramID': 1, 'EventType': '', 'StudyPlan': '', 'StudyType': ''}
# Helper variable for events
eventTable = ['EventID', 'UserID', 'Start', 'End', 'Description', 'ImportanceRanking', 'Title', 'ProgramID', 'EventType', 'StudyPlan', 'StudyType']

#not used in demo
def getEvent(eventID):
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    ret = c.execute("SELECT * FROM event WHERE eventID = {}".format(eventID))
    rowList = []
    for row in ret:
        rowList.append({'EventID':row[0],'Title':row[7],'start':row[1],'end':row[2]})
    
    conn.close()
    return rowList

# Returns a list of events, each event is a dictionary for a given ID
def getUserEvents(userID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    ret = c.execute("SELECT * FROM event WHERE userID = {}".format(userID))
    rowList = []
    for row in ret:
        rowList.append({'EventID':row[0],'Title':row[6],'Start':row[2],'End':row[3], 'StudyType':row[10]})
    
    conn.close()
    return rowList

# Edits an event based on the given ID and the dictionary passed in
def editEvent(eventID,obj):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    t = eventID,
    c.execute('SELECT * FROM event WHERE eventID =?',t)
    r = c.fetchone()
    print(r)
    tempEvent = makeEventDict(r)
    print(tempEvent)
    for col in obj:
        print(col)
        print(obj[col])
        print(tempEvent[col])
        tempEvent[col] = obj[col]
        print(tempEvent[col])
    try:
        c.execute('DELETE FROM event WHERE eventID=?',t)
        c.execute('INSERT INTO event VALUES(:EventID, :UserID, :Start, :End, :Description, :ImportanceRanking, :Title, :ProgramID, :EventType, :StudyPlan, :StudyType)',tempEvent)
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

# Gets a dict with values, changes values of the default event for what needs to be changed
def addNewEvent(obj):     # make sure all information is in the correct formats. Date and Time processing can be done here.
    #format can be copied for all tables
    tempEvent = defaultEvent
    for col in obj:
        tempEvent[col] = obj[col]

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT MAX(eventID) FROM event')
    r = c.fetchone()
    tempEvent['EventID'] = r[0] + 1
    
    try:
        
        c.execute('INSERT INTO event VALUES(:EventID, :UserID, :Start, :End, :Description, :ImportanceRanking, :Title, :ProgramID, :EventType, :StudyPlan, :StudyType)', tempEvent)
        
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
        return tempEvent['EventID']

#Deletes an event and returns the eventID
def deleteEvent(eventID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        t = eventID,
        c.execute('DELETE FROM event WHERE eventID = ?',t)
        
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
        return eventID

# Not implemented demo
def getUser(email):
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = email,
    c.execute("SELECT * FROM user WHERE email = ?", t)
    r = c.fetchone()
    conn.close()
    return r

# Not implemented for demo
def checkLogin(email, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = email,
    print(t)
    c.execute("SELECT hashedpassword FROM user WHERE email = ?", t) 

    r = c.fetchone()
    conn.close()
    if password == r[0]:
        return True
    
    return False

# Not implemented with front end
# Returns the drive link for a specified user
def getDriveLink(email):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    t = email,
    ret = c.execute("SELECT DriveLink FROM user WHERE email = ?", t)
    r = c.fetchone()
    conn.close()
    return r[0]
    
# Not implemented in front end
# Returns an auth key for canvas
def canvasConnect(email):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    t = email,
    ret = c.execute("SELECT CanvasID FROM user WHERE email = ?", t)
    r = c.fetchone()
    conn.close()
    return r[0]
    

'''This method is when we implement multiple users'''
# not implemented for this demo
def addNewUser(obj):
    # make sure all information is in the correct formats. Date and Time processing can be done here
    #format can be copied for all tables

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute('"INSERT INTO user VALUES({}, {}, {}, {}, {}, {}, {}, {}))'.format(obj['UserID'], obj['Email'], obj['FirstName'], obj ['LastName'], obj['Password'], obj['GoogleID'], obj['CanvasID'], obj['DriveLink']))
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

# not implemented for demo
def getProgram(programID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    #need to edit later, perhaps create a 'global' c value, as defined above
    ret = c.execute("SELECT * FROM program WHERE programID = {}".format(programID))
    conn.close()
    return ret

# not implemented for demo
def getStudyLength(StudyType):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    #need to edit later, perhaps create a 'global' c value, as defined above
    c.execute("SELECT * FROM program WHERE programID = 1")
    r = c.fetchone()
    conn.close()

    if StudyType.lower() == 'exam':
        return r[4]
    elif StudyType.lower() == 'assignment':
        return r[5]
    elif StudyType.lower() == 'quiz':
        return r[6]
    else:
        return 1

# Edits the event of the specified ID adding a study plan to it
def editStudyEvent(eventID, StudyPlan):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('UPDATE event SET StudyPlan = ? WHERE EventID = ?',(StudyPlan, eventID))
    conn.close()

# Returns the value of the study plan stored in the DB
def viewStudyPlan(eventID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    t = eventID,
    c.execute("SELECT StudyPlan FROM event WHERE EventID = ?",t)
    r = c.fetchone()
    conn.close()
    return r[0]

# Not implemented for Demo 1
def addNewProgram(obj): 
    # make sure all information is in the correct formats. Date and Time processing can be done here.
    #format can be copied for all tables

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute('"INSERT INTO program VALUES({}, {}, {}, {}, {}, {}, {}))'.format(obj['ProgramID'], obj['UserID'], obj['Description'], obj['Notes'], obj['ExamLength'], obj['AssignmentLength'], obj['QuizLength']))
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

# Helper Method for converting tuple rows into dictionaries
def makeEventDict(row):
    tempEvent = defaultEvent
    x = 0
    for name in eventTable:
        tempEvent[name] = row[x]
        x += 1
    return tempEvent
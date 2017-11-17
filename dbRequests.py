import sqlite3
from sqlite3 import Error
import json

#Name/path of the database
DATABASE = 'test.db'
# Helper variable for events
defaultEvent = {'EventID': -1, 'UserID': 1, 'Start': '2017-10-26T18:53:08Z', 'End': '2017-10-26T19:53:08Z', 'Description': 'An Event', 'ImportanceRanking': 1, 'Title': 'Default Event', 'ProgramID': 1, 'EventType': '', 'StudyPlan': '', 'StudyType': ''}
# Helper variable for events
eventTable = ['EventID', 'UserID', 'Start', 'End', 'Description', 'ImportanceRanking', 'Title', 'ProgramID', 'EventType', 'StudyPlan', 'StudyType']
#Helpervariable for users
defaultUser = {'UserID': 1 , 'email': 'abc123@case.edu', 'FirstName': 'Alpha', 'LastName': 'Cavern', 'HashedPassword': 'hashed', 'GoogleID': -1, 'CanvasID': -1, 'DriveLink': 'https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU'}
#Helpervariable for users
userTable = ['UserID', 'email', 'FirstName', 'LastName', 'HashedPassword', 'GoogleID', 'CanvasID', 'DriveLink']
#Helpervariable for program
defaultProgram = {'ProgramID': 1, 'UserID': 1, 'Description': '', 'Notes': 'https://docs.google.com/document/d/1Aeaj_uiwTcv5IFS2tH7vJcaj2LbMJOO-0dad8l7x98I/edit', 'ExamLength': 3, 'AssignmentLength': 1, 'QuizLength': 2}
#Helpervariable for program
programTable = ['ProgramID', 'UserID', 'Description', 'Notes', 'ExamLength', 'AssignmentLength', 'QuizLength']


#not used in demo
def getEvent(eventID):
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    t = eventID,
    ret = c.execute("SELECT * FROM event WHERE eventID = ?",t)
    rowList = []
    for row in ret:
        rowList.append({'EventID':row[0],'Title':row[6],'Start':row[2],'End':row[3], 'StudyType':row[10]})
    
    conn.close()
    return rowList

# Returns a list of events, each event is a dictionary for a given ID
def getUserEvents(userID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        t = userID,
        ret = c.execute("SELECT * FROM event WHERE userID = ?",t)
        rowList = []
        for row in ret:
            rowList.append({'EventID':row[0],'Title':row[6],'Start':row[2],'End':row[3], 'StudyType':row[10]})
    except Error as e:
        print(e)
    finally:       
        conn.close()
        if(type(rowList) != None):
            return rowList
        return ['Failed']

# Edits an event based on the given ID and the dictionary passed in
def editEvent(eventID,obj):
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    try:
        t = eventID,
        c.execute('SELECT * FROM event WHERE eventID =?',t)
        r = c.fetchone()
        tempEvent = makeEventDict(r)
        for col in obj:
            tempEvent[col] = obj[col]
        c.execute('DELETE FROM event WHERE eventID=?',t)
        c.execute('INSERT INTO event VALUES(:EventID, :UserID, :Start, :End, :Description, :ImportanceRanking, :Title, :ProgramID, :EventType, :StudyPlan, :StudyType)',tempEvent)
        conn.commit()
        retVal = eventID
    except Error as e:
        print(e)
        conn.rollback()
        retVal = e
    finally:
        conn.close()
        return retVal

# Gets a dict with values, changes values of the default event for what needs to be changed
def addNewEvent(obj):     # make sure all information is in the correct formats. Date and Time processing can be done here.

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
        
    try:
        tempEvent = defaultEvent
        for col in obj:
            tempEvent[col] = obj[col]
       
        c.execute('SELECT MAX(eventID) FROM event')
        r = c.fetchone()
        tempEvent['EventID'] = r[0] + 1

        
        c.execute('INSERT INTO event VALUES(:EventID, :UserID, :Start, :End, :Description, :ImportanceRanking, :Title, :ProgramID, :EventType, :StudyPlan, :StudyType)', tempEvent)
        
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
        return str(tempEvent['EventID'])

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
    c.execute("SELECT HashedPassword, UserID FROM user WHERE email = ?", t) 

    r = c.fetchone()
    if r is None:
        return -1
    conn.close()
    if password == r[0]:
        return r[1]
    
    return -1

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
    

def     addNewUser(obj):
    # make sure all information is in the correct formats. Date and Time processing can be done here
    #format can be copied for all tables

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        
        #this checks for the email already existing in the database

        
        #Takes default user and replaces values of the default with the input
        tempUser = defaultUser
        # print(tempUser)
        for col in obj:
            tempUser[col] = obj[col]
        
        #determines the userID for the new user
        c.execute('SELECT MAX(userID) FROM user')
        r = c.fetchone()
        tempUser['UserID'] = r[0] + 1
        # print(tempUser)
        c.execute('INSERT INTO user VALUES(:UserID, :email, :FirstName, :LastName, :HashedPassword, :GoogleID, :CanvasID, :DriveLink)', tempUser)

        conn.commit()
    except Error as e:
        print(e)
        print(type(e))
        writeToLog(e)
        conn.rollback()
    finally:
        conn.close()
        return tempUser['UserID']
    

# not implemented for demo
def getProgram(programID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    #need to edit later, perhaps create a 'global' c value, as defined above
    ret = c.execute("SELECT * FROM program WHERE programID = {}".format(programID))
    conn.close()
    return ret

# Add functionality for programs
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

# Returns the tuple of dicts for all events for study events of a user
#define get study events

# Edits the event of the specified ID adding a study plan to it
def editStudyEvent(eventID, StudyPlan):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute('UPDATE event SET StudyPlan = ? WHERE EventID = ?',(StudyPlan, eventID))
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
        return eventID

# Returns the value of the study plan stored in the DB
def viewStudyPlan(eventID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        t = eventID,
        c.execute("SELECT StudyPlan FROM event WHERE EventID = ?",t)
        r = c.fetchone()
    except Error as e:
        print(e)
    finally:
        conn.close()
        if(type(r) != None):
            return r[0]
        return 'Something went wrong'

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

# Helper Method for converting tuple rows into dictionaries for events
def makeEventDict(row):
    tempEvent = defaultEvent
    x = 0
    for name in eventTable:
        tempEvent[name] = row[x]
        x += 1
    return tempEvent

# Helper Method for converting tuple rows into dictionaries
def makeUserDict(row):
    tempUser = defaultUser
    x = 0
    for name in eventTable:
        tempUser[name] = row[x]
        x += 1
    return tempUser

# Helper Method for converting tuple rows into dictionaries
def makeProgramDict(row):
    tempProgram = defaultProgram
    x = 0
    for name in eventTable:
        tempProgram[name] = row[x]
        x += 1
    return tempProgram

#Preliminary Log file, save the traceback using logging
def writeToLog(inputError):

    file = open("logfile.txt","w") 
    file.write(str(inputError))  
    file.close() 
    print('Hellooo')
    print(inputError.with_traceback())
    
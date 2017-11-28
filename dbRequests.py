import sqlite3
from sqlite3 import Error
import json

#Name/path of the database
DATABASE = 'test.db'
# Helper variable for events
defaultEvent = {'EventID': -1, 'UserID': 1, 'Start': '2017-10-26T18:53:08Z', 'End': '2017-10-26T19:53:08Z', 'Description': 'An Event', 'ImportanceRanking': 1, 'Title': 'Default Event', 'ProgramID': 1, 'EventType': '', 'StudyPlan': '', 'StudyType': '', 'Color': 'blue', 'Recurring': 0}
# Helper variable for events
eventTable = ['EventID', 'UserID', 'Start', 'End', 'Description', 'ImportanceRanking', 'Title', 'ProgramID', 'EventType', 'StudyPlan', 'StudyType', 'Color', 'Recurring']
#Helpervariable for users
defaultUser = {'UserID': 1 , 'email': 'abc123@case.edu', 'FirstName': 'Alpha', 'LastName': 'Cavern', 'HashedPassword': 'hashed', 'GoogleID': -1, 'CanvasID': -1, 'DriveLink': 'https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU'}
#Helpervariable for users
userTable = ['UserID', 'email', 'FirstName', 'LastName', 'HashedPassword', 'GoogleID', 'CanvasID', 'DriveLink']
#Helpervariable for program
defaultProgram = {'ProgramID': 1, 'UserID': 1, 'Description': '', 'Notes': 'https://docs.google.com/document/d/1Aeaj_uiwTcv5IFS2tH7vJcaj2LbMJOO-0dad8l7x98I/edit', 'ExamLength': 3, 'AssignmentLength': 1, 'QuizLength': 2, 'Color': 'blue', 'Title': 'Default Title'}
#Helpervariable for program
programTable = ['ProgramID', 'UserID', 'Description', 'Notes', 'ExamLength', 'AssignmentLength', 'QuizLength', 'Color', 'Title']


#not used in demo
def getEvent(eventID):
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    t = eventID,
    ret = c.execute("SELECT * FROM event WHERE eventID = ?",t)
    rowList = []
    for row in ret:
        rowList.append(makeEventDict(row))
    
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
            rowList.append(makeEventDict(row))
    except Error as e:
        print(e)
    finally:
        conn.close()
        if(type(rowList) is not None):
            return rowList
        return ['Failed']

#Returns all programs for a user
def getUserPrograms(userID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        t = userID,
        ret = c.execute("SELECT * FROM program WHERE userID = ?",t)
        rowList = []
        for row in ret:
            rowList.append(makeProgramDict(row))
    except Error as e:
        print(e)
    finally:       
        conn.close()
        if(type(rowList) is not None):
            return rowList
        return ['Failed']

#Returns all events for a program and a user
def getProgramEvents(userID, programID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        t = userID, programID
        ret = c.execute("SELECT * FROM event WHERE userID = ?, programID =?",t)
        rowList = []
        for row in ret:
            rowList.append(makeEventDict(row))
        
        #manually adds the default program for events to this list
        ret = c.execute("SELECT * FROM event WHERE programID = 1")
        for row in ret:
            rowList.append(makeEventDict(row))
    except Error as e:
        print(e)
    finally:       
        conn.close()
        if(type(rowList) is not None):
            return rowList
        return ['Failed']

#returns a list of dictionaries, values of Program, Events for every program and every event for a user
def getGroupedUserEvents(userID):
    returnList = []
    programList = getUserPrograms(userID)
    for program in programList:
        groupDict = {
            'Program': program,
            'Events': getProgramEvents(userID, program['ProgramID'])
        }
        returnList.append(groupDict)
    return returnList

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
        c.execute('INSERT INTO event VALUES(:EventID, :UserID, :Start, :End, :Description, :ImportanceRanking, :Title, :ProgramID, :EventType, :StudyPlan, :StudyType, :Color, :Recurring)',tempEvent)
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

        
        c.execute('INSERT INTO event VALUES(:EventID, :UserID, :Start, :End, :Description, :ImportanceRanking, :Title, :ProgramID, :EventType, :StudyPlan, :StudyType, :Color, :Recurring)', tempEvent)
        
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
    try:
        t = email,
        c.execute("SELECT * FROM user WHERE email = ?", t)
        r = c.fetchone()
    except Error as e:
        print(e)
    finally:
        conn.close()
        return r

# checks the username and passord sent to the database against what is stored.
def checkLogin(email, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        t = email,
        c.execute("SELECT HashedPassword, UserID FROM user WHERE email = ?", t) 

        r = c.fetchone()
        if r is None:
            return -1
    except Error as e:
        print(e)
    finally:
        conn.close()
        if r is not None and password == r[0]:
            return r[1]        
        return -1

# Not implemented for this demo
# Returns the drive link for a specified user
def getDriveLink(email):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    t = email,
    ret = c.execute("SELECT DriveLink FROM user WHERE email = ?", t)
    r = c.fetchone()
    conn.close()
    return r[0]
    
def setGoogleCredentials(userID, key):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute('UPDATE user SET GoogleID = ? WHERE userID = ?', (key,userID))
        conn.commit()
    except Error as e:
        print(e)
        writeToLog(e)
        conn.rollback()
    finally:
        conn.close()
        return userID

def getGoogleCredentials(userID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        t = userID,
        c.execute('SELECT GoogleID FROM user WHERE userID = ?', t)
        r = c.fetchone()
    except Error as e:
        print(e)
        writeToLog(e)
    finally:
        conn.close()
        if r is not None:
            return r[0]
        else:
            return -1
        

# Not implemented for this demo
# Returns an auth key for canvas
def canvasConnect(email):
    
    # https://canvas.instructure.com/doc/api/calendar_events.html
    # https://canvas.instructure.com/doc/api/file.oauth.html
    # UTech has denied a canvas developer key
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    t = email,
    ret = c.execute("SELECT CanvasID FROM user WHERE email = ?", t)
    r = c.fetchone()
    conn.close()
    return r[0]
    

def addNewUser(obj):
    # make sure all information is in the correct formats. Date and Time processing can be done here
    #format can be copied for all tables

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        
        #this checks for the email already existing in the database

        
        #Takes default user and replaces values of the default with the input
        tempUser = defaultUser
        
        for col in obj:
            tempUser[col] = obj[col]
        
        #determines the userID for the new user
        c.execute('SELECT MAX(userID) FROM user')
        r = c.fetchone()
        tempUser['UserID'] = r[0] + 1
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

#delete a user
def deleteUser(UserID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    try:
        t = UserID,
        c.execute('DELETE FROM user WHERE userID = ?',t)
        c.execute('DELETE FROM program WHERE userID = ?',t)
        c.execute('DELETE FROM event WHERE userID = ?',t)
        
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
        return ProgramID
#Edit a user
def editUser(userID,obj):
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    try:
        t = userID,
        c.execute('SELECT * FROM user WHERE userID =?',t)
        r = c.fetchone()
        tempUser = makeUserDict(r)
        for col in obj:
            tempUser[col] = obj[col]
        c.execute('DELETE FROM user WHERE userID=?',t)
        c.execute('INSERT INTO user VALUES(:UserID, :email, :FirstName, :LastName, :HashedPassword, :GoogleID, :CanvasID, :DriveLink)', tempUser)
        conn.commit()
        retVal = userID
    except Error as e:
        print(e)
        conn.rollback()
        retVal = e
    finally:
        conn.close()
        return retVal

# not implemented for demo
def getProgram(ProgramID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        t = ProgramID,
        c.execute("SELECT * FROM program WHERE ProgramID = ?",t)
        r = c.fetchone()
        ret = makeProgramDict(r)
    except Error as e:
        print(e)
    finally:
        conn.close()
        if type(ret) is not None:
            return ret
        else:
            return 'Failed'

# not implemented for this demo
# Add functionality for programs
def getStudyLength(StudyType, ProgramID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        t = ProgramID,
        c.execute("SELECT * FROM program WHERE ProgramID = ?", t)
        r = c.fetchone()
    except Error as e:
        print(e)
    finally:
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
def getStudyEvents(userID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        ret = c.execute("SELECT * FROM event WHERE StudyType = 'exam' OR StudyType = 'quiz' or StudyType = 'assignment'")
        rowList = []
        for row in ret:
            rowList.append(makeEventDict(row))
    except Error as e:
        print(e)
    finally:       
        conn.close()
        if(type(rowList) is not None):
            return rowList
        return ['Failed']

#not implemented for testing demo
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
        if(type(r) is not None):
            return r[0]
        return 'Something went wrong'

# Not implemented for this demo
def addNewProgram(obj): 
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        tempProgram = defaultProgram
        
        for col in obj:
            tempProgram[col] = obj[col]
        
        c.execute('SELECT MAX(ProgramID) FROM program')
        r = c.fetchone()
        tempProgram['ProgramID'] = r[0] + 1
        c.execute('INSERT INTO program VALUES(:ProgramID, :UserID, :Description, :Notes, :ExamLength, :AssignmentLength, :QuizLength, :Color, :Title)', tempProgram)

        conn.commit()
    except Error as e:
        print(e)
        writeToLog(e)
        conn.rollback()
    finally:
        conn.close()
        return tempProgram['ProgramID']

#Delete an existing program
def deleteProgram(ProgramID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    try:
        t = ProgramID,
        c.execute('DELETE FROM program WHERE programID = ?',t)
        
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
        return ProgramID

#Edit a program
def editProgram(ProgramID,obj):
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    try:
        t = ProgramID,
        c.execute('SELECT * FROM program WHERE programID =?',t)
        r = c.fetchone()
        tempProgram = makeProgramDict(r)
        for col in obj:
            tempProgram[col] = obj[col]
        c.execute('DELETE FROM program WHERE programID=?',t)
        c.execute('INSERT INTO program VALUES(:ProgramID, :UserID, :Description, :Notes, :ExamLength, :AssignmentLength, :QuizLength, :Color, :Title)', tempProgram)
        conn.commit()
        retVal = ProgramID
    except Error as e:
        print(e)
        conn.rollback()
        retVal = e
    finally:
        conn.close()
        return retVal

# Helper Method for converting tuple rows into dictionaries for events
def makeEventDict(row):
    tempEvent = defaultEvent.copy()
    x = 0
    for name in eventTable:
        tempEvent[name] = row[x]
        x += 1
    return tempEvent

# Helper Method for converting tuple rows into dictionaries
def makeUserDict(row):
    tempUser = defaultUser.copy()
    x = 0
    for name in userTable:
        tempUser[name] = row[x]
        x += 1
    return tempUser

# Helper Method for converting tuple rows into dictionaries
def makeProgramDict(row):
    tempProgram = defaultProgram.copy()
    x = 0
    for name in programTable:
        tempProgram[name] = row[x]
        x += 1
    return tempProgram

#Preliminary Log file, save the traceback using logging
def writeToLog(inputError):

    file = open("logfile.txt","w") 
    file.write(str(inputError))  
    file.close() 
    print('An error has been written to the log')
    print(inputError.with_traceback())
    
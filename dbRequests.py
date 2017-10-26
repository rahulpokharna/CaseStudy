import sqlite3
from sqlite3 import Error
import json

DATABASE = 'test.db'
defaultEvent = {'EventID': -1, 'UserID': 1, 'Start': '2017-10-26T18:53:08Z', 'End': '2017-10-26T19:53:08Z', 'Description': 'An Event', 'ImportanceRanking': 1, 'Title': 'Default Event', 'ProgramID': -1, 'EventType': '', 'StudyPlan': '', 'StudyType': ''}
    
def getEvent(eventID):
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    ret = c.execute("SELECT * FROM event WHERE eventID = {}".format(eventID))
    rowList = []
    for row in ret:
        rowList.append({'EventID':row[0],'Title':row[7],'start':row[1],'end':row[2]})
    
    conn.close()
    return rowList

def getUserEvents(userID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    ret = c.execute("SELECT * FROM event WHERE userID = {}".format(userID))
    rowList = []
    for row in ret:
        rowList.append({'EventID':row[0],'Title':row[6],'Start':row[2],'End':row[3]})
    
    conn.close()
    return rowList

#TODO
def editEvent(eventID,obj):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    t = eventID,
    c.execute('SELECT * FROM event WHERE eventID =?',t)
    r = c.fetchone()
    tempEvent = makeEventDict(r)
    for col in obj:
        tempEvent[col] = obj[col]
    try:
        c.execute('DELETE FROM event WHERE eventID=?',t)
        c.execute('INSERT INTO event VALUES(:EventID, :UserID, :Start, :End, :Description, :ImportanceRanking, :Title, :ProgramID, :EventType, :StudyPlan, :StudyType)',tempEvent)
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

# Gets a dict with values of 9EventID, UserID, Time, Length, Date, Description, ImportanceRanking, Title, ProgramID , EventType, StudyPlan, StudyType) AS A DICT
def addNewEvent(obj):     # make sure all information is in the correct formats. Date and Time processing can be done here.
    #format can be copied for all tables
    tempEvent = defaultEvent
    for thing in obj:
        tempEvent[thing] = obj[thing]

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        
        c.execute('INSERT INTO event VALUES(:EventID, :UserID, :Start, :End, :Description, :ImportanceRanking, :Title, :ProgramID, :EventType, :StudyPlan, :StudyType)', tempEvent)
        
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

def getUser(email):
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = email,
    c.execute("SELECT * FROM user WHERE email = ?", t)
    r = c.fetchone()
    conn.close()
    return r

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

def getDriveLink(email):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    t = email,
    ret = c.execute("SELECT DriveLink FROM user WHERE email = ?", t)
    r = c.fetchone()
    conn.close()
    return r[0]
    

'''This method is when we implement multiple users'''
# input is dict with values (UserID, email, FirstName, LastName, Password, GoogleID, CanvasID, DriveLink)
def addNewUser(obj):
    # make sure all information is in the correct formats. Date and Time processing can be done here
    #format can be copied for all tables

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute('"INSERT INTO user VALUES({}, {}, {}, {}, {}, {}, {}, {}))'.format(obj['UserID'], obj['email'], obj['FirstName'], obj ['LastName'], obj['Password'], obj['GoogleID'], obj['CanvasID'], obj['DriveLink']))
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

def getProgram(programID):
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    #need to edit later, perhaps create a 'global' c value, as defined above
    ret = c.execute("SELECT * FROM program WHERE programID = {}".format(programID))
    conn.close()
    return ret


def getStudyLength(programID, studyType):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    #need to edit later, perhaps create a 'global' c value, as defined above
    c.execute("SELECT * FROM program WHERE programID = {}".format(programID))
    r = c.fetchone()
    conn.close()

    if studyType.lower() == 'exam':
        return r[4]
    elif studyType.lower() == 'assignment':
        return r[5]
    elif studyType.lower() == 'quiz':
        return r[6]
    else:
        return 1

#input is dict with values of (ProgramID, UserID, Description, Notes, ExamLength, AssignmentLength, QuizLength)
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

def makeEventDict(row):
    tempEvent = defaultEvent
    x = 0
    for col in tempEvent:
        tempEvent[col] = row[x]
        x += 1
    return tempEvent
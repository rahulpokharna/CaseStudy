import sqlite3
from sqlite3 import Error
import json

DATABASE = 'new.db'

def getEvent(eventID):
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    #need to edit later, perhaps create a 'global' c value, as defined above
    ret = c.execute("SELECT * FROM event WHERE eventID = {}".format(eventID))
    conn.close()
    return ret

def getUserEvents(userID):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    #need to edit later, perhaps create a 'global' c value, as defined above
    ret = c.execute("SELECT * FROM event WHERE userID = {}".format(userID))
    conn.close()

    for row in ret:
        print(row)
    return ret
# Gets a dic with values of 9EventID, UserID, Time, Length, Date, Description, ImportanceRanking, Title, ProgramID , EventType, StudyPlan, StudyType) AS A DICT

def addNewEvent(obj):     # make sure all information is in the correct formats. Date and Time processing can be done here.
    #format can be copied for all tables

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute('"INSERT INTO event VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}))'.format(obj['EventID'], obj['UserID'], obj['Time'], obj['Length'], obj['Date'], obj['Description'], obj['ImportanceRanking'], obj['Title'], obj['ProgramID'] , obj['EventType'], obj['StudyPlan'], obj['StudyType']))
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

def getUser(email):
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    #need to edit later, perhaps create a 'global' c value, as defined above
    ret = c.execute("SELECT * FROM user WHERE email = {}".format(email))
    conn.close()
    return ret

def checkLogin(email, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    #need to edit later, perhaps create a 'global' c value, as defined above
    ret = c.execute("SELECT * FROM user WHERE email = {}".format(email))
    conn.close()

    if password == ret[5]:
        return True
    
    return False

def getDriveLink(email):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    #need to edit later, perhaps create a 'global' c value, as defined above
    ret = c.execute("SELECT * FROM user WHERE email = {}".format(email))
    conn.close()
    return ret[8]

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
    ret = c.execute("SELECT * FROM program WHERE programID = {}".format(programID))
    conn.close()

    if studyType == 'exam':
        return ret[5]
    elif studyType == 'assignment':
        return ret[6]
    elif studyType == 'quiz':
        return ret[7]
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

import sqlite3
from sqlite3 import Error
import collections
import dbRequests
#File path/name of database file to be read
DATABASE = 'test.db'




def initDB():
    """ Initialize the database with the specified tables and other information """
    #Connection to the database
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:

        '''initialize the Tables'''
        c.execute('''CREATE TABLE event(EventID integer, UserID integer, Start text, End text, Description text, ImportanceRanking integer, Title text, ProgramID integer, EventType text, StudyPlan text, StudyType text) ''')
        c.execute('''CREATE TABLE program(ProgramID integer, UserID integer, Description text, Notes text, ExamLength integer, AssignmentLength integer, QuizLength integer)''')
        c.execute('''CREATE TABLE user(UserID integer, email text, FirstName text, LastName text, HashedPassword text, GoogleID text, CanvasID text, DriveLink text)''')


        conn.commit()

    except Error as e:
        print(e)
    finally:
        conn.close()
        
def fillDB():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    '''Add Test Values to Tables'''
    try:
        '''
        c.execute("SELECT count(*) FROM user")
        r = c.fetchone()

        c.execute("INSERT INTO user VALUES ({},'abc123@case.edu','Alpha', 'Cavern','hashed','','','https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU')".format(r[0] + 1))
        
        c.execute("INSERT INTO user VALUES ({},'axc1223@case.edu','Andrew', 'Clark','hashed','','','https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU')".format(r[0] + 2))
        c.execute("INSERT INTO user VALUES ({},'yxs123@case.edu','Yongju', 'Sui','hashed','','','https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU')".format(r[0] + 3))

        '''

        c.execute("SELECT count(*) FROM user")
        r = c.fetchone()
        c.execute("INSERT INTO event VALUES ({}, 0001,'Start Time', 'End Time','this is annoying',4,'Test Event 2', -1,'One Time', '','')".format(r[0] + 1))
        c.execute("INSERT INTO event VALUES ({}, 0001,'1 Time', '1 Time','this is great',4,'Test Event a2', -1,'One Time', '','')".format(r[0] + 2))
        c.execute("INSERT INTO event VALUES ({}, 0001,'Start 1', 'End 1','this is sad',4,'Test Event 2aa', -1,'One Time', '','')".format(r[0] + 3))

        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()

def queryDB():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    '''Test Queries'''
    #test for printing
    nameTuple = ()
    c.execute("SELECT count(*) FROM event")
    r = c.fetchone()
    eventDict = {
        'EventID' :3,
        'Title' : 'No Longer a Test',
        'Start' : '2017-10-26T22:53:08Z',
        'End' : '2017-10-26T18:53:08Z'
    }
    nameTuple = tuple(eventDict.values())
    '''    print(eventDict)
    print(eventDict.items())
    print(nameTuple)'''
    dbRequests.addNewEvent(eventDict)

    #Editing Event Here
    #dbRequests.editEvent(eventDict['EventID'], eventDict)

    '''values = dbRequests.checkLogin('abc123@case.edu','hashed')
    print('Here are the events for the user')
    
    print(values)'''

    '''
    c.execute("SELECT count(*) FROM user")
    r = c.fetchone()
    num = r[0]
    c.execute("SELECT * FROM user")
    for x in range(num):
        r = c.fetchone()
        print(r)

    for row in c.execute("SELECT * FROM user"):
        print(type(row))
        for col in row:
            print(type(col))
        print()

    c.execute("SELECT * FROM user")
    names = [description[0] for description in c.description]
    print(names)

    print(type(c.execute("SELECT * FROM user")))
    ''' 
    conn.close()



if __name__ == '__main__':
    #initDB()
    #fillDB()
    queryDB()
import sqlite3
from sqlite3 import Error
 
DATABASE = 'new.db'
def initDB(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        '''initialize the Tables'''
        #c.execute('''CREATE TABLE event(EventID integer, UserID integer, Start text, End text, Description text, ImportanceRanking integer, Title text, ProgramID integer, EventType text, StudyPlan text, StudyType text) ''')
        #c.execute('''CREATE TABLE program(ProgramID integer, UserID integer, Description text, Notes text, ExamLength integer, AssignmentLength integer, QuizLength integer)''')
        #c.execute('''CREATE TABLE user(UserID integer, email text, FirstName text, LastName text, HashedPassword text, GoogleID text, CanvasID text, DriveLink text)''')
        
        '''Add Test Values to Tables'''
        #c.execute("INSERT INTO user VALUES (0001'abc123@case.edu','Alpha', 'Cavern','hashed','','','https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU')")
        #c.execute("INSERT INTO user VALUES (0002'axc1223@case.edu','Andrew', 'Clark','hashed','','','https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU')")
        #c.execute("INSERT INTO user VALUES (0003,'yxs123@case.edu','Yongju', 'Sui','hashed','','','https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU')")
        
        c.execute("INSERT INTO event VALUES (0002, 0001,'Start Time', 'End Time','this is annoying',4,'Test Event 2', -1,'One Time', '','')")
        
        '''Test Queries'''
        #for row in c.execute("SELECT email FROM user"):
        #    print(row)
        #c.execute('')
        


        conn.commit()

    except Error as e:
        print(e)
    finally:
        conn.close()
 
def getEvent(givenID):
    
    #need to edit later, perhaps create a 'global' c value, as defined above
     return c.execute("SELECT * FROM event WHERE eventID = '%s'" % givenID)

if __name__ == '__main__':
    initDB(DATABASE)
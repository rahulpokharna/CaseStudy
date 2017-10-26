import sqlite3
from sqlite3 import Error
 
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
        test = 0
        numUsers = c.execute('''SELECT count(*) FROM user''')
        nums = c.fetchone()
        print(nums)

        for x in numUsers:
            print(x)
            test = x
            
        print(test)
        
        c.execute("INSERT INTO user VALUES (?,'abc123@case.edu','Alpha', 'Cavern','hashed','','','https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU')", (nums))
        '''
        c.execute("INSERT INTO user VALUES ({},'axc1223@case.edu','Andrew', 'Clark','hashed','','','https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU')".format(numUsers + 2))
        c.execute("INSERT INTO user VALUES ({},'yxs123@case.edu','Yongju', 'Sui','hashed','','','https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU')".format(numUsers + 3))

        numEvents = c.execute("SELECT count(*) FROM event")

        c.execute("INSERT INTO event VALUES ({}}, 0001,'Start Time', 'End Time','this is annoying',4,'Test Event 2', -1,'One Time', '','')".format(numEvents + 1))
'''
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
    for row in c.execute("SELECT * FROM user"):
        for col in row:
            print(col)
        print()
    conn.close()

if __name__ == '__main__':
    #initDB()
    #fillDB()
    queryDB()
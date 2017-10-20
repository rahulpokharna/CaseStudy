import sqlite3
from sqlite3 import Error
 
#File path/name of database file to be read
DATABASE = 'new.db'




def initDB(db_file):
    """ Initialize the database with the specified tables and other information """
    #Connection to the database
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:

        '''initialize the Tables'''
        #c.execute('''CREATE TABLE event(EventID integer, UserID integer, Start text, End text, Description text, ImportanceRanking integer, Title text, ProgramID integer, EventType text, StudyPlan text, StudyType text) ''')
        #c.execute('''CREATE TABLE program(ProgramID integer, UserID integer, Description text, Notes text, ExamLength integer, AssignmentLength integer, QuizLength integer)''')
        #c.execute('''CREATE TABLE user(UserID integer, email text, FirstName text, LastName text, HashedPassword text, GoogleID text, CanvasID text, DriveLink text)''')
        
        '''Add Test Values to Tables'''
        '''
        c.execute("INSERT INTO user VALUES (0001,'abc123@case.edu','Alpha', 'Cavern','hashed','','','https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU')")
        c.execute("INSERT INTO user VALUES (0002,'axc1223@case.edu','Andrew', 'Clark','hashed','','','https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU')")
        c.execute("INSERT INTO user VALUES (0003,'yxs123@case.edu','Yongju', 'Sui','hashed','','','https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU')")
        '''
        #c.execute("INSERT INTO event VALUES (0002, 0001,'Start Time', 'End Time','this is annoying',4,'Test Event 2', -1,'One Time', '','')")
        
        '''Test Queries'''
        
        #test for printing
        for row in c.execute("SELECT * FROM user"):
            for col in row:
                print(col)
            print()
        


        conn.commit()

    except Error as e:
        print(e)
    finally:
        conn.close()
        

if __name__ == '__main__':
    initDB(DATABASE)
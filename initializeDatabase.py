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
        c.execute('''CREATE TABLE event(EventID integer, UserID integer, Start text, End text, Description text, ImportanceRanking integer, Title text, ProgramID integer, EventType text, StudyPlan text, StudyType text, Color text, Recurring integer) ''')
        c.execute('''CREATE TABLE program(ProgramID integer, UserID integer, Description text, Notes text, ExamLength integer, AssignmentLength integer, QuizLength integer)''')
        c.execute('''CREATE TABLE user(UserID integer, email text, FirstName text, LastName text, HashedPassword text, GoogleID text, CanvasID text, DriveLink text, Color text, Title text)''')


        conn.commit()

    except Error as e:
        print(e)
    finally:
        conn.close()

if __name__ == '__main__':
    initDB()
import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE event(eventID integer, userID integer, Start text, End text, Description text, ImportanceRanking integer, Title text, ProgramID integer, EventType text, StudyPlan text, StudyType text) ''')
        c.execute('''CREATE TABLE program(ProgramID integer, UserID integer, Description text, Notes text, ExamLength integer, AssignmentLength integer, QuizLength integer)''')
        c.execute('''CREATE TABLE user(UserID integer, email text, FirstName text, LastName text, HashedPassword text, GoogleID text, CanvasID text, DriveLink text)''')
        print('Hello')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()
 
if __name__ == '__main__':
    create_connection('new.db')
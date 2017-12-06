import sqlite3
from sqlite3 import Error
import collections
import dbRequests
#File path/name of database file to be read
DATABASE = 'test.db'
from requestHelpers import *

def hash():
    """ Initialize the database with the specified tables and other information """
    #Connection to the database
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:

        rows = c.execute('SELECT hashedpassword, userID from user where userid == 9')
        for row in rows:
            updateDict = {'HashedPassword': row[0], 'UserID': row[1]}
            newPass = row[0]
            #hash password here
            updateDict['HashedPassword'] = hashString(newPass)
            c.execute('UPDATE user set HashedPassword = :HashedPassword WHERE userID = :UserID', updateDict)
            conn.commit()


    except Error as e:
        print(e)
    finally:
        conn.close()

if __name__ == '__main__':
    hash()
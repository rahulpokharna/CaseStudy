import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import unittest
import sqlite3
from sqlite3 import Error
import dbRequests
class TestAppMethods(unittest.TestCase):

    testUser = {'UserID': 20 , 'email': 'ext23@case.edu', 'FirstName': 'Eeeeeeee', 'LastName': 'Teeeeee', 'HashedPassword': 'hashed', 'GoogleID': -1, 'CanvasID': -1, 'DriveLink': 'https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU'}
    testEvent = {'EventID': -1, 'UserID': 20, 'Start': '2017-10-26T18:53:08Z', 'End': '2017-10-26T19:53:08Z', 'Description': 'An Event', 'ImportanceRanking': 1, 'Title': 'Default Event', 'ProgramID': 1, 'EventType': '', 'StudyPlan': '', 'StudyType': ''}
    testEvent2 = {'EventID': -2, 'UserID': 20, 'Start': '2017-11-26T18:53:08Z', 'End': '2017-11-26T19:53:08Z', 'Description': 'An Event 2', 'ImportanceRanking': 1, 'Title': 'Default Event', 'ProgramID': 1, 'EventType': '', 'StudyPlan': '', 'StudyType': ''}

    def setUp(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute('INSERT INTO user VALUES(:UserID, :email, :FirstName, :LastName, :HashedPassword, :GoogleID, :CanvasID, :DriveLink)', self.testUser)
        c.execute('INSERT INTO event VALUES(:EventID, :UserID, :Start, :End, :Description, :ImportanceRanking, :Title, :ProgramID, :EventType, :StudyPlan, :StudyType)', self.testEvent)
        c.execute('INSERT INTO event VALUES(:EventID, :UserID, :Start, :End, :Description, :ImportanceRanking, :Title, :ProgramID, :EventType, :StudyPlan, :StudyType)', self.testEvent2)
        conn.commit()
        conn.close()

    #Unit test for getting an event
    def testGetEvent(self):
       response = dbRequests.getEvent(-1)
       assert response[0].items() <= self.testEvent.items()

       response = dbRequests.getEvent(-2)
       assert response[0].items() <= self.testEvent2.items()

    #unit test for getting all events for a user
    def testGetUserEvents(self):
        response = dbRequests.getUserEvents(20)
        self.assertTrue(response[0].items() <= self.testEvent.items())
        self.assertTrue(response[1].items() <= self.testEvent2.items())

    #unit test for edit event
    def testEditEvent(self):
        editedEvent = {'EventID': -1, 'UserID': 20, 'Start': '2017-10-26T20:53:08Z', 'End': '2017-10-26T23:53:08Z', 'Description': 'An Event', 'ImportanceRanking': 1, 'Title': 'Edited Event', 'ProgramID': 1, 'EventType': '', 'StudyPlan': '', 'StudyType': ''}
        dbRequests.editEvent(-1,editedEvent)
        response = dbRequests.getEvent(-1)
        assert response[0].items() <= editedEvent.items()
        self.assertFalse(response[0].items() <= self.testEvent.items())

    def testAddNewEvent(self):
        newEvent = {'EventID': 23, 'UserID': 12, 'Start': '2017-11-28T20:53:08Z', 'End': '2017-11-28T23:53:08Z', 'Description': 'An Event', 'ImportanceRanking': 1, 'Title': 'New Added Event', 'ProgramID': 1, 'EventType': '', 'StudyPlan': '', 'StudyType': ''}
        dbRequests.addNewEvent(newEvent)
        #since we already tested get event, we can use it again here
        validate = dbRequests.getEvent(23) #23 because I manually checked the DB
        self.assertTrue(validate[0].items() <= newEvent.items())
        self.assertFalse(validate[0].items() <= self.testEvent.items())
        self.assertFalse(validate[0].items() <= self.testEvent2.items())

    def testDeleteEvent(self):
        dbRequests.deleteEvent(-2)
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        #use sql to get the supposed event with the id -2
        c.execute('SELECT * FROM event WHERE EventID = -2')
        r = c.fetchone()
        #if r itself has the type of none, assert true since the event should be deleted
        self.assertTrue(r is None)

        dbRequests.deleteEvent(-1)
        c.execute('SELECT * FROM event WHERE EventID = -1')
        r = c.fetchone()
        self.assertTrue(r is None)

        conn.close()
        
    #Unit test for chceking log in
    def testCheckLogin(self):
        response = dbRequests.checkLogin('ext23@case.edu', 'hashed')
        self.assertTrue(response == 20)
        response = dbRequests.checkLogin('ext23@case.edu', 'password')
        self.assertTrue(response == -1)
        response = dbRequests.checkLogin('ext23@case.edu', 'test')
        self.assertTrue(response == -1)

    # Uinit test for adding a user
    def testAddNewUser(self):
        newUser = {'UserID': 21 , 'email': 'sxd10@case.edu', 'FirstName': 'Shiv', 'LastName': 'Desai', 'HashedPassword': 'pword', 'GoogleID': '-1', 'CanvasID': '-1', 'DriveLink': 'https://drive.google.com/open?id=0B8WM6XnQ3RJ6RS1XUzNfLVNnQlU'}
        dbRequests.addNewUser(newUser)
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute('SELECT * FROM user WHERE userID = 21')
        r = c.fetchone()
        userDict = dbRequests.makeUserDict(r)
        self.assertTrue(userDict.items() <= newUser.items())

    #to be run after completion of setup
    def tearDown(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("DELETE FROM user WHERE userID = 20")
        c.execute("DELETE FROM user WHERE userID = 21")
        c.execute("DELETE FROM event WHERE eventID = -1")
        c.execute("DELETE FROM event WHERE eventID = -2")
        c.execute("DELETE FROM event WHERE userID = 12")
        conn.commit()
        conn.close()
   
if __name__ == '__main__':
    unittest.main()
    
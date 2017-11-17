
# Bring your packages onto the path
import sqlite3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import unittest
import app
import json
import flask
import dbRequests
class TestAppMethods(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.userId = dbRequests.addNewUser({'email': 'sibiistesting@case.edu', 'FirstName': 'Luigi', 'LastName': 'Mario', 'HashedPassword': 'hashed'})
        self.event1Id = dbRequests.addNewEvent({'UserID': self.userId, 'Start': '2017-10-26T18:53:08Z', 'End': '2017-10-26T19:53:08Z', 'Description': 'An Event', 'ImportanceRanking': 1, 'Title': 'TestEvent1', 'ProgramID': 1, 'EventType': '', 'StudyPlan': '', 'StudyType': ''})
        self.event2Id = dbRequests.addNewEvent({'UserID': self.userId, 'Start': '2017-10-26T18:53:08Z', 'End': '2017-10-26T19:53:08Z', 'Description': 'An Event', 'ImportanceRanking': 1, 'Title': 'TestEvent2', 'ProgramID': 1, 'EventType': '', 'StudyPlan': '', 'StudyType': ''})
        # self.testEventID = int(response.data.decode("utf-8"))


    def testIndexIfLoggedIn(self):
        with self.app.session_transaction() as sess:
            sess['logged_in'] = True
            sess['email'] = 'sibiistesting@case.edu'
        response = self.app.get('/')
        #redirect to calendar
        assert 'target URL: <a href="/calendar">/calendar</a>' in str(response.data)

    def testIndexIfNotLoggedIn(self):
        with self.app.session_transaction() as sess:
            sess['logged_in'] = False
        response = self.app.get('/')
        #redirect to login
        assert 'target URL: <a href="/welcome">/welcome</a>' in str(response.data)

    def testCalendarIfLoggedIn(self):
        with self.app.session_transaction() as sess:
            sess['logged_in'] = True
            sess['email'] = 'sibiistesting@case.edu'
        response = self.app.get('/calendar')
        #redirect to calendar
        assert 'CalendarChild' in str(response.data)

    def testCalendarIfNotLoggedIn(self):
        with self.app.session_transaction() as sess:
            sess['logged_in'] = False
        response = self.app.get('/calendar')
        # redirect to login
        assert 'target URL: <a href="/welcome">/welcome</a>' in str(response.data)

    def testWelcomePage(self):
        response = self.app.get('/welcome')
        assert 'WelcomePage' in str(response.data)

    def testLoginPassing(self):
        response = self.app.post('/login', data=dict(
            email='sibiistesting@case.edu',
            password='hashed'
        ))
        # check if the user redirected to the correct page
        # print(response.data)
        assert 'target URL: <a href="/calendar">/calendar</a>' in str(response.data)

    def testLoginIncorrectPassword(self):
        response = self.app.post('/login', data=dict(
            email='sibiistesting@case.edu',
            password='notpassword'
        ))
        # check if the user redirected to the correct page
        assert 'target URL: <a href="/welcome">/welcome</a>' in str(response.data)

    def testLoginIncorrectEmail(self):
            response = self.app.post('/login', data=dict(
                email='sibiistestingFAKE@case.edu',
                password='hashed'
            ))
            # check if the user redirected to the correct page
            assert 'target URL: <a href="/welcome">/welcome</a>' in str(response.data)

    def testLogout(self):
        with app.app.test_client() as c:
            response = c.get('/logout')
            assert not flask.session['logged_in'] and 'target URL: <a href="/welcome">/welcome</a>' in str(response.data)


    def testGetUserEvents(self):
        #test getting all events for a user.
        response = self.app.get('/request/events?userID={}'.format(self.userId))
        #just check if the user has multiple events.
        s = json.loads(response.data.decode("utf-8"))
        assert len(s) == 2

    def testGetUserEventWithNoEvents(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("DELETE FROM event WHERE userID = {}".format(self.userId))
        conn.commit()
        conn.close()
        #test getting all events for a user.
        response = self.app.get('/request/events?userID={}'.format(self.userId))
        #just check if the user has multiple events.
        s = json.loads(response.data.decode("utf-8"))
        assert len(s) == 0

    def testGetEvent(self):
        #test getting a specific event for a user.
        response = self.app.get('/request/events?eventID={}'.format(self.event1Id))
        #check if the event ID we get back is the same one we asked for.
        assert json.loads(response.data.decode('utf-8'))[0]['Title'] == "TestEvent1"

    def testGetEventWithInvalidEvent(self):
        #test getting a specific event for a user.
        response = self.app.get('/request/events?eventID={}'.format(-1))
        #check if the event ID we get back is the same one we asked for.
        assert response.data.decode("utf-8") == '[]\n'
    # def testEditEvent(self):
    #     response = self.app.post('/request/events', data=dict(
    #         id = self.testEventID,
    #         title = 'test',
    #         start = 2,
    #         end = '3'
    #     ))
    #     #get back the event we just editted
    #     #just checking the event ID here. Im having issues with checking the acutal attributes.
    #     assert int(response.data.decode('utf-8')) == self.testEventID
    def testDeleteEvent(self):
        #delete the event
        response = self.app.get('/request/events?eventID={}&delete=true'.format(self.event1Id))
        #try getting it again
        response = self.app.get('/request/events?eventID={}'.format(self.event1Id))
        #check that the get request now returns empyt list :)
        assert response.data.decode("utf-8") == '[]\n'

    def testGoingToRegisterPage(self):
        response = self.app.get('/register')
        #check if the form is onthe page.
        assert 'form id="registration"' in str(response.data)

    def testRegisteringNewUser(self):
        response = self.app.post('/register', data=dict(
            email='sibiistestingNEW@case.edu',
            HashedPassword='hashed',
            FirstName='Luke',
            LastName='SkyWalker',
        ))
        #redirect to login screeeen
        assert 'target URL: <a href="/welcome">/welcome</a>' in str(response.data)

    def testRegisteringNewUserWhoAlreadyExists(self):
        response = self.app.post('/register', data=dict(
            email='sibiistesting@case.edu',
            HashedPassword='hashed',
            FirstName='Luke',
            LastName='SkyWalker',
        ))
        #redirect to login screeeen
        assert 'target URL: <a href="/register">/register</a>' in str(response.data)


    def tearDown(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("DELETE FROM user WHERE userID = {}".format(self.userId))
        c.execute("DELETE FROM event WHERE userID = {}".format(self.userId))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    unittest.main()
    
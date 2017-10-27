
# Bring your packages onto the path
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import unittest
import app
import json
class TestAppMethods(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        


    def testIndex(self):
       response = self.app.get('/')
       #just make sure the page we get has a login button on it, because that means it is probably the login page.
       assert 'input type=submit value=Login>' in str(response.data)

    def testLoginPassing(self):
        response = self.app.post('/login', data=dict(
            email='email',
            password='password'
        ))
        # check if the user redirected to the correct page
        # print(response.data)
        assert 'kian' in str(response.data)
    
    def testLoginFailing(self):
        response = self.app.post('/login', data=dict(
            email='WrongEmail',
            password='WrongPassword'
        ))
        # check if the user redirected to the correct page
        # print(response.data)
        # we should be redirected back to the login page.
        assert 'target URL: <a href="/">/</a>' in str(response.data)
    
    def testGetUserEvents(self):
        #test getting all events for a user.
        response = self.app.get('/request/events?userID=1')
        #just check if the user has multiple events.
        s = response.data.decode("utf-8")
        assert len(json.loads(s)) > 1

    def testGetEvent(self):
        #test getting a specific event for a user.
        response = self.app.post('/request/events', data=dict(
            title = 'testEvetn',
            start = 1,
            end = 2
        ), follow_redirects=True)
        # self.testEventID = response.data
        print(response.data)
if __name__ == '__main__':
    unittest.main()
    
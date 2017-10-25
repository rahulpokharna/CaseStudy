
# Bring your packages onto the path
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import unittest
import app
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
        print(response.data)
        assert 'kian' in str(response.data)

if __name__ == '__main__':
    unittest.main()
    
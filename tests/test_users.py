import unittest, sys, os

#sys.path.append('../seo-week-4')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main1 import app, db

class UsersTests(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    ###############
    #### tests ####
    ###############

    def register(self, username, password):
        return self.app.post('/register',
                            data=dict(username=username,
                                      password=password, 
                                      confirm_password=password),
                            follow_redirects=True)


    def login(self, username, password):
        return self.app.post('/login',
                             data=dict(username=username,
                                       password=password),
                             follow_redirects=True)


    def test_valid_user_registration(self):
        response = self.register('test', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_username_registration(self):
        response = self.register('t', 'FlaskIsAwesome')
        self.assertIn(b'Field must be between 2 and 20 characters long.', response.data)

    def test_invalid_password_registration(self):
        response = self.register('test2', '1')
        self.assertIn(b'Field must be between 8 and 20 characters long.', response.data)


if __name__ == "__main__":
    unittest.main()

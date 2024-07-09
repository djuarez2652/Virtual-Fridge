import unittest, sys, os

sys.path.append('../seo-week-4')
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

    def test_valid_user_registration(self):
        response = self.register('test', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_username_registration(self):
        response = self.register('t', 'FlaskIsAwesome')
        self.assertIn(b'Field must be between 2 and 20 characters long.', response.data)

    def test_invalid_password_registration(self):
        response = self.register('test2', '1')
        self.assertIn(b'Password must be between 8 and 20 characters long.', response.data)


    def add_stock(self, item_name, expire_date):
        return self.app.post('/stock',
                             data=dict(item_name=item_name,
                                       expire_date=expire_date),
                             follow_redirects=True)

    def test_valid_item(self):
        response = self.add_stock('Apple', '10-12-2024')
        self.assertEqual(response.status_code, 200)

    def test_invalid_item_name(self):
        response = self.add_stock('a', '10-12-2024')
        self.assertIn(b'Field must be between 2 and 20 characters long.', response.data)


if __name__ == "__main__":
    unittest.main()

import unittest, sys, os

sys.path.append('../seo-week-4')
from main1 import *

class UnitTests(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
    
    def test_insert_food(self):
        with self.assertRaises(Exception):
            insert_food(-1, 'goldfish', '12-12-1212')

    def test_has_food(self):
        with self.assertRaises(Exception):
            has_food(-1)
        

if __name__ == '__main__':
    unittest.main()
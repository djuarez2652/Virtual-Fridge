from main1 import *
import unittest
import sys
import os

sys.path.append('../seo-week-4')


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

    def test_query_stock(self):
        with self.assertRaises(Exception):
            query_stock(-1)

    def test_remove_food(self):
        with self.assertRaises(Exception):
            remove_food(-1)


if __name__ == '__main__':
    unittest.main()

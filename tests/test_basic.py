import unittest, sys

sys.path.append('../seo-week-4') # imports python file from parent directory
from main1 import app #imports flask app object

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        #print(response)
        self.assertEqual(response.status_code, 200)

    def register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        #print(response)
        self.assertEqual(response.status_code, 200)

    def crazy_page(self):
        response = self.app.get('/crazy', follow_redirects=True)
        #print(response)
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
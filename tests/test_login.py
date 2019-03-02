import os
import unittest,requests
from flask import Flask
TEST_DB = 'test.db'
app = Flask(__name__)
class BasicTests(unittest.TestCase): 
###############
#### tests ####
###############
	def test_main_page(self):
		url = "http://0.0.0.0:4310/login"
		data = {'userID': "-1"}
		r = requests.post(url, data)
		self.assertEqual(r.status_code, 200)
 
 
if __name__ == "__main__":
	unittest.main()

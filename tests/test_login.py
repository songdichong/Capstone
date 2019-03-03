'''
Original Author: Dichong Song
Creation date: Mar 2, 2019
Contents of file: 
	Unit testing of login
'''
import unittest,requests
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

'''
Original Author: Yuhan Ye
Creation date: Mar 2, 2019
Contents of file: 
	Unit testing of register
'''

import unittest, requests
class BasicTests(unittest.TestCase):
###################################
############ tests ################
#### Run website.py before test####
###################################
	def test_main_page(self):
		url = 'http://0.0.0.0:4310/register'
		data = {'positionNumber': "0","goToSignUp":"0"}
		r = requests.post(url, data)
		self.assertEqual(r.status_code, 200)


if __name__ == "__main__":
	unittest.main()

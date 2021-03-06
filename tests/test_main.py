'''
Original Author: Dichong Song
Creation date: Mar 2, 2019
Contents of file: 
	Unit testing of main
'''
import unittest,requests
class BasicTests(unittest.TestCase): 
###################################
############ tests ################
#### Run website.py before test####
###################################
	def test_main_page(self):
		url = "http://0.0.0.0:4310/"
		r = requests.get(url)
		self.assertEqual(r.status_code, 200)
 
	def test_post_page(self):
		url = "http://0.0.0.0:4310/"
		data = {'request': "3"}
		r = requests.post(url,data)
		self.assertEqual(r.status_code, 200)
 
if __name__ == "__main__":
	unittest.main()

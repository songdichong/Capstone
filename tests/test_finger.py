'''
Original Author: Dichong Song
Creation date: April 7, 2019
Contents of file: 
	Unit testing of run fingerprint
'''
import unittest,requests
class BasicTests(unittest.TestCase): 
###############################################
################ tests ########################
#### Run fingerprint_handler.py before test####
###############################################
	def test_main_page(self):
		url = "http://0.0.0.0:4311/search"
		data = {'data': "1"}
		r = requests.post(url, data)
		self.assertEqual(r.status_code, 200)
		#fingerprint should be running
		
		url = "http://0.0.0.0:4311/exit"
		r = requests.post(url, data)
		self.assertEqual(r.status_code, 200)
		#fingerprint should be shut down
		
		url = "http://0.0.0.0:4311/register"
		r = requests.post(url, data)
		self.assertEqual(r.status_code, 200)
		#fingerprint should be running
if __name__ == "__main__":
	unittest.main()

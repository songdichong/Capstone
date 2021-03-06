'''
Original Author: Yue Ma
Creation date: Mar 2, 2019
Contents of file: 
	Unit testing of signup
'''
import unittest, requests
class BasicTests(unittest.TestCase):
####################################
############ tests #################
#### Run website.py before test#####
####################################
    def test_signup_page(self):
        url = "http://0.0.0.0:4310/signup"
        data = {'gml': "test@gmail.com",'uname':'YuGa'}
        r = requests.post(url, data)
        self.assertEqual(r.status_code, 200)


if __name__ == "__main__":
    unittest.main()

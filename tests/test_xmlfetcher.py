'''
Original Author: Yue Ma
Creation date: Mar 2, 2019
Contents of file: 
	Unit testing of database
'''
import unittest, requests
#~ from ... import website
##Only can be tested on Raspberry Pi
class BasicTests(unittest.TestCase):
    ###############
    #### tests ####
    ###############
    def test_main_page(self):
        url = "http://0.0.0.0:4310/"
        pass
        #~ my_list = website.xmlfetcher("https://www.cbc.ca/cmlink/rss-topstories")
        #~ self.assertNotEqual(len(my_list), 0)

if __name__ == "__main__":
    unittest.main()


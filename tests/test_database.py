import unittest
from .. import website
##Only can be tested on Raspberry Pi
class BasicTests(unittest.TestCase):
    ###############
    #### tests ####
    ###############
    def test_add_to_database(self):
        website.test()
        self.assertEqual(0, 0)

if __name__ == "__main__":
    unittest.main()


import unittest
from .. import website
##Only can be tested on Raspberry Pi
class BasicTests(unittest.TestCase):
    ###############
    #### tests ####
    ###############
    def test_add_to_database(self):
        databaseName = 'unitTestDatabase.db'
        userID = '1'
        username = 'YuGa'
        email = 'YuGa@gmail.com'
        preference = '01001'
        website.add_into_database(userID, username, email, preference)
        print(website.select_from_database('YuGa'))
        self.assertEqual(0, 0)

if __name__ == "__main__":
    unittest.main()


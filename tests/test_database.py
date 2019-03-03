import unittest
import website
##Only can be tested on Raspberry Pi
class BasicTests(unittest.TestCase):
    ###############
    #### tests ####
    ###############
    def test_add_to_database(self):
        databaseName = 'unitTestDatabase.db'
        website.createTable(databaseName)
        userID = '1'
        username = 'YuGa'
        email = 'YuGa@gmail.com'
        preference = '01001'
        website.add_into_database(userID, username, email, preference,databaseName)
        queryResult = website.select_from_database(userID,databaseName)
        self.assertEqual(queryResult, (1, 'YuGa', 'YuGa@gmail.com', 1001))

if __name__ == "__main__":
    unittest.main()


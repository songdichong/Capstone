import unittest, requests


class BasicTests(unittest.TestCase):
    ###############
    #### tests ####
    ###############
    def test_main_page(self):
		url = "http://0.0.0.0:4310/register"
		data = {'positionNumber': "2"}
		r = requests.post(url, data)
		self.assertEqual(r.status_code, 200)


if __name__ == "__main__":
    unittest.main()

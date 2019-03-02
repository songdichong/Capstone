import unittest

from myapp import config
from myapp import create_app

class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config.TEST_DATABASE_URI)
        self.client = self.app.test_client()
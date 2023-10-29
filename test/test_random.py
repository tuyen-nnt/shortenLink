import unittest
from utils import constant
from utils.random_url import get_random_url

class TestGenerateRandomPath(unittest.TestCase):
    def test_length_path(self):
        actual = len(get_random_url(num=constant.URL_LENGTH))
        self.assertEqual(constant.URL_LENGTH, actual)

    def test_type_path(self):
        actual = get_random_url(num=constant.URL_LENGTH)
        self.assertEqual(type("str"), type(actual))

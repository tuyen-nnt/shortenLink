import random
import string
import unittest
import constant


def get_random_url(num):
    if num == 0:
        return ''
    else:
        # https://stackoverflow.com/questions/2823316/generate-a-random-letter-in-python
        return random.choice(string.ascii_letters) + get_random_url(num - 1)


class TestGenerateRandomPath(unittest.TestCase):
    def test_length_path(self):
        actual = len(get_random_url(num=constant.URL_LENGTH))
        self.assertEqual(constant.URL_LENGTH, actual)

    def test_type_path(self):
        actual = get_random_url(num=constant.URL_LENGTH)
        self.assertEqual(type("str"), type(actual))

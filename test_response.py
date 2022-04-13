import unittest
import url_handler

class TestGetResponse(unittest.TestCase):
    def test_get_response(self):
        handler = url_handler.UrlShortenHandler()
        handler.write('http://localhost:8080/?id=UeuhX')

        self.resp = handler.get()
        assert self.resp is handler.redirect("https://google.com")

#!/usr/bin/python3
# Làm sao để tạo form input vào link và nó trả về kết quả. Sau đó bấm link kết quả và sẽ redirect qua trang đã input

import tornado.ioloop
import tornado.web
import hashlib
import random
import string
import subprocess

URL_LENGTH = 5

# Dict này lưu cặp shorten: real_url
URL = {}
# Dict này ngược lại lưu hash_url:shorten
URL_REVERSE = {}


def get_random_url(num):
    if num == 0:
        return ''
    else:
        # https://stackoverflow.com/questions/2823316/generate-a-random-letter-in-python
        return random.choice(string.ascii_letters) + get_random_url(num - 1)


class UrlShortenHandler(tornado.web.RequestHandler):

    # VD như postman chọn method POST thì nó sẽ chạy hàm này
    def post(self):

        host = self.request.headers.get('Host')
        print('Host: ' + host)

        #Nhập input, url is a parameter. Hàm dưới đây giúp truy xuất tham số trong body của Post.
        url = self.get_body_argument("url", default=None, strip=False)
        # url = self.get_query_argument("url", default=None, strip=False)
        # https://stackoverflow.com/questions/34818996/tornado-what-is-the-difference-between-requesthandlers-get-argument-get-qu
        # url = self.request.body.decode('utf-8')
        # Hàm Hash dùng để băm ra 1 chuỗi có độ dài cố định từ chuỗi url đầu vào tránh nó dài hay ngắn quá. Param của nó phải là định dạng byte. DO vậy phải encode()
        # https://dancongngheorg.wordpress.com/2018/08/29/cach-tao-ham-bam-voi-python/
        #     encode() : Converts the string into bytes to be acceptable by hash function.
        #     digest() : Returns the encoded data in byte format.
        #     hexdigest() : Returns the encoded data in hexadecimal format.

        hash = hashlib.md5(url.encode()).hexdigest()

        # Check xem cái key có trong dict (db) không, nếu có thì in ra shorten link đã tạo luôn
        if hash in URL_REVERSE:
            # write result
            self.write('http://' + host + '/shorten?id=' + URL_REVERSE[hash])
            return

        # Nếu chưa có thì tạo random shorten link
        shorten = get_random_url(URL_LENGTH)
        # KHi mà shorten đã được tạo bởi url khác rồi thì tiếp tục tạo shorten khác
        while shorten in URL:
            shorten = get_random_url(URL_LENGTH)

        print("Receive url: " + url)
        print("Shorten url: " + shorten)
        print("Hash url: " + hash)

        URL[shorten] = url
        # Hash key of the dict is a hex(url)
        URL_REVERSE[hash] = shorten
        self.write('http://' + host + '/shorten?id=' + shorten)
    # As long as you use the port as setup here, the method will run this script
    def get(self):
        id = self.get_argument('id', default=None)
        if id in URL:
            #self.write(URL[id])
            self.redirect(URL[id])
        else:
            self.clear()
            self.set_status(404)
            self.finish('')


    def head(self):
        id = self.get_argument('id', default=None)
        if id in URL:
            #self.write(URL[id])
            self.redirect(URL[id])
        else:
            self.clear()
            self.set_status(404)
            self.finish('')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Tuyen Nguyen')
        # subprocess.call("echo Hello World", shell=True)


def make_app():
    return tornado.web.Application([
        (r"/(index\.html)", tornado.web.StaticFileHandler, {'path': '.'}),
        (r"/shorten", UrlShortenHandler),
        (r"/", IndexHandler),
    ]
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


# import webbrowser
# REDIRECT: webbrowser.open('http://example.com')

# https://www.youtube.com/watch?v=DQNW9qhl4eA
# https://www.youtube.com/watch?v=-gJ21qzpieA
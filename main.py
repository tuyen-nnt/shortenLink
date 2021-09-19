#!/usr/bin/python3
# Làm sao để tạo form input vào link và nó trả về kết quả. Sau đó bấm link kết quả và sẽ redirect qua trang đã input

import tornado.ioloop
import tornado.web
import hashlib
import random
import string
import sqlite3
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
    # When you submit the info, the page would use method POST
    def post(self):

        host = self.request.headers.get('Host')
        print('Host: ' + host)

        # Nhập input, url is a parameter. Hàm dưới đây giúp truy xuất attribute name="url" trong body khi gọi phương thức Post ở index.html file.
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

        # connect to the database
        db = sqlite3.connect('url.db')
        cursor = db.cursor()

        # create table if not exists
        cursor.execute("""CREATE TABLE IF NOT EXITS myurl(
                ... id INTEGER PRIMARY KEY,
                ... real_url VARCHAR,
                ... hash_url VARCHAR,
                ... shorten_url VARCHAR
                ... )""")

        # Check xem cái hash url có trong db không, nếu có thì in ra shorten link đã tạo luôn
        cursor.execute("SELECT shorten_url FROM myurl WHERE hash_url = ?", (hash,))
        # fetch the first result of the query above (tuple type)
        result = cursor.fetchone()
        print(result)

        if result and len(result) > 0:
            # write result, this is the this.responseText you can see in index.html file
            self.write('http://' + host + '/shorten?id=' + result[0])
            return


        # Nếu chưa có trong db thì tạo random shorten link
        shorten = get_random_url(URL_LENGTH)
        # Khi mà shorten đã được tạo bởi url khác rồi thì tiếp tục tạo shorten khác
        cursor.execute("SELECT id FROM myurl WHERE shorten_url = ?", (shorten,))
        # fetch the first result of the query above
        result = cursor.fetchone()

        # if the result is already created, we will continue generating
        while result and len(result) > 0:
            shorten = get_random_url(URL_LENGTH)
            cursor.execute("SELECT id FROM myurl WHERE shorten_url = ?", (shorten,))
            # fetch the first result of the query above
            result = cursor.fetchone()

        print("Receive url: " + url)
        print("Shorten url: " + shorten)
        print("Hash url: " + hash)

        params = (url, hash, shorten)
        cursor.execute("INSERT INTO myurl (id, real_url, hash_url, shorten_url) VALUES (NULL , ?, ?, ?)", params)
        self.write('http://' + host + '/shorten?id=' + shorten)

        db.commit()
        db.close()

    # When the page retrieve the result, the method will use method GET
    def get(self):
        # connect to the database
        db = sqlite3.connect('url.db')
        cursor = db.cursor()
        # Lấy id query trong url. This is just shorten character.
        id = self.get_argument('id', default=None)
        cursor.execute("SELECT real_url FROM myurl WHERE shorten_url = ?", (id,))
        # fetch the first result of the query above
        result = cursor.fetchone()

        # print(type(result))
        # print(result[0])

        print(result and len(result) > 0)

        if result and len(result) > 0:
            self.redirect(result[0])
        else:
            self.clear()
            self.set_status(404)
            self.finish('')
        db.close()

    def head(self):
        # connect to the database
        db = sqlite3.connect('url.db')
        cursor = db.cursor()
        # Lấy id query trong url. This is just shorten character.
        id = self.get_argument('id', default=None)
        cursor.execute("SELECT real_url FROM myurl WHERE shorten_url = ?", (id,))
        # fetch the first result of the query above
        result = cursor.fetchone()

        if result and len(result) > 0:
            self.redirect(result[0])
        db.close()

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

# SQLite3 Database : https://www.udacity.com/blog/2021/07/how-to-write-your-first-python-application.html
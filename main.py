#!/usr/bin/python3
# Làm sao để tạo form input vào link và nó trả về kết quả. Sau đó bấm link kết quả và sẽ redirect qua trang đã input

import hashlib
import os

import tornado.ioloop
import tornado.web

import backend_db


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Tuyen Nguyen')
        # subprocess.call("echo Hello World", shell=True)

def make_app():
    # https://www.devart.com/dbforge/mysql/how-to-install-mysql-on-ubuntu/
    db = backend_db.MyDatabase(
        host=os.getenv('DB_HOST', 'localhost'),
        # https://stackoverflow.com/questions/4906977/how-to-access-environment-variable-values
        port=int(os.getenv('DB_PORT', 3306)),
        username=os.getenv('DB_USER', 'tuyen'),
        password=os.getenv('DB_PASSWORD', 'Password@123'),
        db_name=os.getenv('DB_NAME', 'shortlink')
    )

    class UrlShortenHandler(tornado.web.RequestHandler):

        def initialize(self, database):
            self.database = database

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


            db.add_url(self, host, url, hash)



        # When the page retrieve the result, the method will use method GET
        def get(self):
            id = self.get_argument('', default=None)
            db.get_url(self, id)

        def head(self):
            id = self.get_argument('', default=None)
            db.get_url(self, id)


    # https://www.tornadoweb.org/en/stable/web.html
    return tornado.web.Application([
            (r"/(index\.html)", tornado.web.StaticFileHandler, {'path': '.'}),
            (r"/", UrlShortenHandler, dict(database=db)),
            (r"/index", IndexHandler),
        ])


# https://www.tornadoweb.org/en/stable/index.html

'''
# To create link
$ curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "url=https://abc.com" http://localhost:8080
http://localhost:8080/?=ROCZc
'''

'''
# To verify
$ curl -v "http://localhost:8080/?=ROCZc"
*   Trying ::1:8080...
* Connected to localhost (::1) port 8080 (#0)
> GET /?=ROCZc HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.77.0
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 302 Found
< Server: TornadoServer/6.1
< Content-Type: text/html; charset=UTF-8
< Date: Sat, 26 Mar 2022 11:34:42 GMT
< Location: https://abc.com                 <<<<<< ---------------------
< Content-Length: 0
<
* Connection #0 to host localhost left intact
'''
if __name__ == "__main__":
    app = make_app()

    port = int(os.getenv('WEB_LISTEN_PORT', '8080'))
    app.listen(port=port)
    print('Server is listening at port ' + str(port))

    tornado.ioloop.IOLoop.current().start()

# https://thaythuocdonghanh.vn/sf8s7fsufasjf/create_link
# http://127.0.0.1/create_link
# import webbrowser
# REDIRECT: webbrowser.open('http://example.com')

# https://www.youtube.com/watch?v=DQNW9qhl4eA
# https://www.youtube.com/watch?v=-gJ21qzpieA

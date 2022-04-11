import tornado.ioloop
import tornado.web
import hashlib
import backend_db
from random_url import get_random_url
import constant


# Dict này lưu cặp shorten: real_url
URL = {}
# Dict này ngược lại lưu hash_url:shorten
URL_REVERSE = {}

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

        result = self.database.check_url(hash)
        if result:
            print("Receive url: " + url)
            print("Shorten url: " + result[0])
            print("Hash url: " + hash)
            return self.write('http://' + host + '/?id=' + result[0])

        result_random = self.database.check_gen_random()
        print(result_random)

        self.database.add_url(url, hash, result_random)

        self.write('http://' + host + '/?id=' + result_random)


    # When the page retrieve the result, the method will use method GET
    def get(self):
        id = self.get_argument('id', default=None)
        print(id)
        result = self.database.get_url(id)

        if result and len(result) > 0:
            self.redirect(result[0])
        else:
            self.clear()
            self.set_status(404)
            self.finish('')

    def head(self):
        id = self.get_argument('id', default=None)
        result = self.database.get_url(id)

        if result and len(result) > 0:
            self.redirect(result[0])
        else:
            self.clear()
            self.set_status(404)
            self.finish('')

# https://www.tornadoweb.org/en/stable/web.html
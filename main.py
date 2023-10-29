#!/usr/bin/python3
# Làm sao để tạo form input vào link và nó trả về kết quả. Sau đó bấm link kết quả và sẽ redirect qua trang đã input
import environs
import tornado.ioloop
import tornado.web
import os
from database import MyDatabase as Orm
from api import url_handler, index_handler


env = environs.Env()
env.read_env('.env')
URL_LENGTH = 5

def make_app():
    # https://stackoverflow.com/questions/4906977/how-to-access-environment-variable-values
    db = Orm.MyDatabase(
        host=env.str("MYSQL.HOST"),
        port=3306,
        username=env.str("MYSQL.DBUSER"),
        password=env.str("MYSQL.PASSWORD"),
        db_name=env.str("MYSQL.DBNAME")
    )


    return tornado.web.Application([
            (r"/(index\.html)", tornado.web.StaticFileHandler, {'path': '.'}),
            (r"/", url_handler.UrlShortenHandler, dict(database=db)),
            (r"/index", index_handler.IndexHandler),
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

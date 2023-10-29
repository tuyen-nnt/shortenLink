import tornado.web

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Tuyen Nguyen')
        # subprocess.call("echo Hello World", shell=True)
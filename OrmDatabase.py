from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, create_engine, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy_utils import create_database, database_exists
import constant
import random_url

# Instruction
# https://stackoverflow.com/questions/10770377/how-to-create-db-in-mysql-with-sqlalchemy
# https://stackoverflow.com/questions/6506578/how-to-create-a-new-database-using-sqlalchemy/30971098#30971098
# class Base(DeclarativeBase):
#     pass

class MyDatabase:
    def __init__(self, host, port, username, password, db_name):
        url = 'mysql://{0}:{1}@{2}:{3}/{4}'.format(username, password, host, port, db_name)
        if not database_exists(url):
            create_database(url)
        # connect to server
        self.engine = create_engine(url, echo=True).connect()

        # id: Mapped[int] = mapped_column(primary_key=True)
        # real_url: Mapped[str] = mapped_column(String(80))
        # hash_url: Mapped[str] = mapped_column(String(80))
        # shorten_url: Mapped[str] = mapped_column(String(50))
        # def __repr__(self) -> str:
        #     return f"User(id={self.id!r}, real_url={self.real_url!r}, shorten_url={self.shorten_url!r})"
        print("Connected to MySQL database at %s:%s" % (host, port))



    def check_url(self, hash):
        # Check xem cái hash url có trong db không, nếu có thì in ra shorten link đã tạo luôn
        result = self.engine.execute(text("SELECT shorten_url FROM myurl WHERE hash_url = {0}".format(hash))).fetchone()
        # fetch the first result of the query above (tuple type)
        if result and len(result) > 0:
            # write result, this is the this.responseText you can see in index.html file
            return result
        else:
            print("Not in Database yet")


    def check_gen_random(self):
        shorten = random_url.get_random_url(constant.URL_LENGTH)
        print("test: " + shorten)
        # Khi mà shorten đã được tạo bởi url khác rồi thì tiếp tục tạo shorten khác
        result_random = self.engine.execute(text("SELECT id FROM myurl WHERE shorten_url = {0}".format(shorten))).fetchone()
        # fetch the first result of the query above
        print(result_random)
        while result_random and len(result_random) > 0:
            shorten = random_url.get_random_url(constant.URL_LENGTH)
            print("test: " + shorten)
            # Khi mà shorten đã được tạo bởi url khác rồi thì tiếp tục tạo shorten khác
            # fetch the first result of the query above
            result_random = self.engine.execute(text("SELECT id FROM myurl WHERE shorten_url = {0}".format(shorten))).fetchone()

        return shorten

    def add_url(self, url, hash, shorten):
        params = (url, hash, shorten)
        self.engine.execute(text("INSERT INTO myurl (real_url, hash_url, shorten_url) VALUES ({0}, {1}, {2})".format(url, hash, shorten))).fetchone()
        self.engine.commit()
        # self.engine.close()

        print("Receive url: " + url)
        print("Shorten url: " + shorten)
        print("Hash url: " + hash)
        return print("Done new insertion to database!")



    def get_url(self, id):

        # Lấy id query trong url. This is just shorten character.
        result = self.engine.execute(text("SELECT real_url FROM myurl WHERE shorten_url ={0}".format(id))).fetchone()
        # fetch the first result of the query above
        # print(type(result))
        # print(result[0])
        # self.connection.close()
        return result

from sqlalchemy import URL
import urllib.parse

from sqlalchemy import URL
from sqlalchemy import create_engine, select, insert
from sqlalchemy.orm import declarative_base

import constant
import random_url
from database.models.base import Base
from database.models.myurl import MyURL
import database.models.setup as setup




# Instruction
# https://stackoverflow.com/questions/10770377/how-to-create-db-in-mysql-with-sqlalchemy
# https://stackoverflow.com/questions/6506578/how-to-create-a-new-database-using-sqlalchemy/30971098#30971098
# class Base(DeclarativeBase):
#     pass


class MyDatabase:
    def __init__(self, host, port, username, password, db_name):
        # url = f'mysql+pymysql://{username}:{urllib.parse.quote(password)}@{host}:{port}/{db_name}'


        self.engine = setup.create_engine_url(host, port, username, password, db_name)
        Base.metadata.create_all(self.engine, checkfirst=True)

        self.session_pool = setup.create_session_pool(self.engine)

        # try:
        #     # suppose the database has been restarted.
        #     self.engine.execute(text("SELECT * FROM shortlink"))
        #     self.engine.close()
        # except exc.DBAPIError as e:
        #     # an exception is raised, Connection is invalidated.
        #     if e.connection_invalidated:
        #         print("Connection was invalidated!")

        print("Connected to MySQL database at %s:%s" % (host, port))

        # self.engine.execute(text("USE shortlink"))

        # create table if not exists
        # self.engine.execute(text("CREATE TABLE IF NOT EXISTS myurl (id INTEGER NOT NULL primary key AUTO_INCREMENT,\
        #                     real_url VARCHAR(100), \
        #                     hash_url VARCHAR(100), \
        #                     shorten_url VARCHAR(100) \
        # )"))


    def check_url(self, hash):
        # Check xem cái hash url có trong db không, nếu có thì in ra shorten link đã tạo luôn
        with self.session_pool() as session:
            result = session.execute(select(MyURL.shorten_url).where(MyURL.hash_url == hash)).first()
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
        with self.session_pool() as session:
            result_random = session.execute(
                select(MyURL.id).where(MyURL.shorten_url == shorten)).first()

        # fetch the first result of the query above
        print(result_random)

        while result_random and len(result_random) > 0:
            shorten = random_url.get_random_url(constant.URL_LENGTH)
            print("test: " + shorten)
            # Khi mà shorten đã được tạo bởi url khác rồi thì tiếp tục tạo shorten khác
            # fetch the first result of the query above
            with self.session_pool() as session:
                result_random = session.execute(
                    select(MyURL.id).where(MyURL.shorten_url == shorten)).first()

        return shorten

    def add_url(self, url, hash, shorten):
        # newRow = Shortlink(real_url={url}, hash_url={hash}, shorten_url={shorten})
        # self.session.add(newRow)
        with self.session_pool() as session:
            act = insert(MyURL).values(real_url=url, hash_url=hash, shorten_url=shorten)
            session.execute(act)
            session.commit()
            session.close()

        print("Receive url: " + url)
        print("Shorten url: " + shorten)
        print("Hash url: " + hash)
        return print("Done new insertion to database!")



    def get_url(self, id):
        with self.session_pool() as session:
            result = session.execute(
                select(MyURL.id).where(MyURL.shorten_url == id)).first()
        # Lấy id query trong url. This is just shorten character.
        # result = self.engine.execute(text("SELECT real_url FROM myurl WHERE shorten_url ={0}".format(id))).fetchone()
        # fetch the first result of the query above
        # print(type(result))
        # print(result[0])
        # self.connection.close()
        return result

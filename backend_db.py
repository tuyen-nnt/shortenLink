#!/usr/bin/python3

import mysql.connector
import tornado.ioloop
import tornado.web
import hashlib
import random
import os
import string

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

class MyDatabase:

    def __init__(self, host, port, username, password, db_name):
        print("host=%s, port=%d, username=%s, password=%s, db_name=%s" % (host, port, username, password, db_name))

        self.connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=db_name
        )

        # https://realpython.com/python-string-formatting/
        print("Connected to MySQL database at %s:%s" % (host, port))

        self.cursor = self.connection.cursor()

        # create table if not exists
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS shortlink")

        self.cursor.execute("USE shortlink")

        # create table if not exists
        self.cursor.execute("CREATE TABLE IF NOT EXISTS myurl (id INTEGER NOT NULL primary key AUTO_INCREMENT,\
                            real_url VARCHAR(100), \
                            hash_url VARCHAR(100), \
                            shorten_url VARCHAR(100) \
        )")

    # TODO: Write all methods that allow create shorten urls and get real urls from shorten url
    def add_url(self, UrlShortenHandler, host, url, hash):
        cursor = self.cursor()

        # Check xem cái hash url có trong db không, nếu có thì in ra shorten link đã tạo luôn
        cursor.execute("SELECT shorten_url FROM myurl WHERE hash_url = %s", (hash,))
        # fetch the first result of the query above (tuple type)
        result = cursor.fetchone()

        if result and len(result) > 0:
            # write result, this is the this.responseText you can see in index.html file
            self.connection.commit()
            self.connection.close()
            print("Receive url: " + url)
            print("Shorten url: " + result[0])
            print("Hash url: " + hash)
            return UrlShortenHandler.write('http://' + host + '/?=' + result[0])


        # Nếu chưa có trong db thì tạo random shorten link
        shorten = get_random_url(URL_LENGTH)
        # Khi mà shorten đã được tạo bởi url khác rồi thì tiếp tục tạo shorten khác
        cursor.execute("SELECT id FROM myurl WHERE shorten_url = %s", (shorten,))
        # fetch the first result of the query above
        result = cursor.fetchone()

        # if the result is already created, we will continue generating
        while result and len(result) > 0:
            shorten = get_random_url(URL_LENGTH)
            cursor.execute("SELECT id FROM myurl WHERE shorten_url = %s", (shorten,))
            # fetch the first result of the query above
            result = cursor.fetchone()

        params = (url, hash, shorten)
        cursor.execute("INSERT INTO myurl (real_url, hash_url, shorten_url) VALUES (%s, %s, %s)", params)
        self.connection.commit()
        self.connection.close()

        print("Receive url: " + url)
        print("Shorten url: " + shorten)
        print("Hash url: " + hash)

        return UrlShortenHandler.write('http://' + host + '/?=' + shorten)



    def get_url(self, UrlShortenHandler, id):

        # Lấy id query trong url. This is just shorten character.
        cursor = self.cursor()
        cursor.execute("SELECT real_url FROM myurl WHERE shorten_url = %s", (id,))
        # fetch the first result of the query above
        result = cursor.fetchone()

        # print(type(result))
        # print(result[0])
        self.connection.close()

        if result and len(result) > 0:
            UrlShortenHandler.redirect(result[0])
        else:
            UrlShortenHandler.clear()
            UrlShortenHandler.set_status(404)
            UrlShortenHandler.finish('')

#!/usr/bin/python3

import mysql.connector
import tornado.ioloop
import tornado.web
import hashlib
import random_url
import os
import string
import constant
from url_handler import UrlShortenHandler


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

    def check_url(self, hash):
        cursor = self.cursor
        # Check xem cái hash url có trong db không, nếu có thì in ra shorten link đã tạo luôn
        cursor.execute("SELECT shorten_url FROM myurl WHERE hash_url = %s", (hash,))
        # fetch the first result of the query above (tuple type)
        result = cursor.fetchone()
        if result and len(result) > 0:
            # write result, this is the this.responseText you can see in index.html file
            return result
        else:
            print("Not in Database yet")


    def check_gen_random(self):
        shorten = random_url.get_random_url(constant.URL_LENGTH)
        print("test: " + shorten)
        # Khi mà shorten đã được tạo bởi url khác rồi thì tiếp tục tạo shorten khác
        self.cursor.execute("SELECT id FROM myurl WHERE shorten_url = %s", (shorten,))
        # fetch the first result of the query above
        result_random = self.cursor.fetchone()
        print(result_random)
        while result_random and len(result_random) > 0:
            shorten = random_url.get_random_url(constant.URL_LENGTH)
            print("test: " + shorten)
            # Khi mà shorten đã được tạo bởi url khác rồi thì tiếp tục tạo shorten khác
            self.cursor.execute("SELECT id FROM myurl WHERE shorten_url = %s", (shorten,))
            # fetch the first result of the query above
            result_random = self.cursor.fetchone()

        return shorten

    def add_url(self, url, hash, shorten):
        cursor = self.cursor
        params = (url, hash, shorten)
        cursor.execute("INSERT INTO myurl (real_url, hash_url, shorten_url) VALUES (%s, %s, %s)", params)
        self.connection.commit()
        self.connection.close()

        print("Receive url: " + url)
        print("Shorten url: " + shorten)
        print("Hash url: " + hash)
        return print("Done new insertion to database!")



    def get_url(self, id):

        # Lấy id query trong url. This is just shorten character.
        cursor = self.cursor
        cursor.execute("SELECT real_url FROM myurl WHERE shorten_url = %s", (id,))
        # fetch the first result of the query above
        result = cursor.fetchone()
        # print(type(result))
        # print(result[0])
        # self.connection.close()
        return result



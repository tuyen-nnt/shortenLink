#!/usr/bin/python3

import mysql.connector


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
        self.cursor.execute("CREATE TABLE IF NOT EXISTS myurl (id INTEGER NOT NULL primary key AUTO_INCREMENT,\
                            real_url VARCHAR(100), \
                            hash_url VARCHAR(100), \
                            shorten_url VARCHAR(100) \
        )")

    # TODO: Write all methods that allow create shorten urls and get real urls from shorten url
    def add_url(self, url):
        '''

        :param url:
        :return:
        '''

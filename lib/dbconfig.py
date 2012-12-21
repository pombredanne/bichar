#!/usr/bin/env python

import sqlite3


class DatabaseDriver(object):
    """
    """
    def __init__(self):
        pass

    def setup(self):
        """opens a connection to the sqlite db
        """
        self.conn = sqlite3.connect('db/bichar.db')
        self.cur = self.conn.cursor()

    def ensure_table(self):
        """ensures that table exists inside database
        """
        table_ensure_sql = "CREATE TABLE IF NOT EXISTS tweets(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, tweet TEXT, label varchar(10))"
        self.cur.execute(table_ensure_sql)

    def teardown(self):
        """closes connection to the db
        """
        self.conn.close()

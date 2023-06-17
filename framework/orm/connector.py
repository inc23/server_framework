import sqlite3
import os
from framework.settings import db_dir_path, db_name


class DBConnector:

    def __init__(self):
        db_path = os.path.join(db_dir_path, db_name)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_connector(self):
        return self.conn

    def fetch(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def create(self, query, *args):
        print(args)
        args = [None, *args]
        self.cursor.execute(query, args)
        self.conn.commit()

    def update(self, query):
        self.cursor.execute(query)
        self.conn.commit()


connector = DBConnector()
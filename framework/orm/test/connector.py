import sqlite3
import os


class DBConnector:

    def __init__(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        bd_path = os.path.join(dir, 'tutorial.db')
        self.conn = sqlite3.connect(bd_path)
        self.cursor = self.conn.cursor()

    def fetch(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def create(self, query, *args):
        args = [None, *args]
        self.cursor.execute(query, args)
        self.conn.commit()

    def update(self, query):
        self.cursor.execute(query)
        self.conn.commit()


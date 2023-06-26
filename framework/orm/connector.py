import sqlite3
import os
from framework import settings


class DBConnector:

    def __init__(self):
        db_path = os.path.join(settings.db_dir_path, settings.db_name)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_connector(self):
        return self.conn

    def fetch(self, query: str) -> list:
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def create(self, query: str, *args) -> None:
        self.cursor.execute(query, args)
        self.conn.commit()

    def update(self, query: str) -> None:
        self.cursor.execute(query)
        self.conn.commit()


connector = DBConnector()
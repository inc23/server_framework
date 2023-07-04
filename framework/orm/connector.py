import sqlite3
import os
from framework import settings


class DBConnector:

    def __init__(self):
        db_path = os.path.join(settings.db_dir_path, settings.db_name)
        self._conn = sqlite3.connect(db_path)
        self._cursor = self._conn.cursor()

    def get_connector(self):
        return self._conn

    def fetch(self, query: str) -> list:
        self._cursor.execute(query)
        return self._cursor.fetchall()

    def create(self, query: str, *args) -> None:
        self._cursor.execute(query, args)
        self._conn.commit()

    def update(self, query: str) -> None:
        self._cursor.execute(query)
        print(query)
        self._conn.commit()


connector = DBConnector()
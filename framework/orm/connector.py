import sqlite3
import os
import settings


class DBConnector:

    def __init__(self):
        db_path = os.path.join(settings.db_dir_path, settings.db_name)
        self._conn = sqlite3.connect(db_path)

    def get_connector(self):
        return self._conn

    def fetch(self, query: str) -> list:
        cursor = self._conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def create(self, query: str, *args) -> None:
        cursor = self._conn.cursor()
        cursor.execute(query, args)
        self._conn.commit()
        cursor.close()

    def update(self, query: str) -> None:
        cursor = self._conn.cursor()
        cursor.execute(query)
        self._conn.commit()
        cursor.close()


connector = DBConnector()
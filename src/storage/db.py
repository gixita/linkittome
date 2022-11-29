import sqlite3
from contextlib import closing


def db() -> str:
    return 'links.db'


def execute(command: str):
    with closing(sqlite3.connect(db())) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(command)
            connection.commit()


def db_fetchone(command: str):
    with closing(sqlite3.connect(db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            return cursor.execute(command).fetchone()


def db_fetchall(command: str):
    with closing(sqlite3.connect(db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            return cursor.execute(command).fetchall()


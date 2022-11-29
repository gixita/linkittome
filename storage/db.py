import sqlite3
from contextlib import closing


def db() -> str:
    return 'links.db'


def execute(command: str):
    with closing(sqlite3.connect(db())) as connection:
        with closing(connection.cursor()) as cursor:
            return cursor.execute(command)


def db_fetchone(command: str):
    return execute.fetchone()


def db_fetchall(command: str):
    return execute.fetchall()

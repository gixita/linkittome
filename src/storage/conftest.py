import pytest
from src.storage import session, word, db
import sqlite3
from contextlib import closing


@pytest.fixture()
def setup_db_examples():
    session.add_session('2', '3', '4', 1, 3)
    session.add_session("ca9366d7-7e20-4148-9e6f-ebb92d1436a8",
                        "b7a0a52c-86eb-4e5c-a9e2-ba8194e2c571",
                        "ae2a5d59-3158-4132-a80f-6a0ab682ba2b", 1, 3)
    word.add_word("screw", 1, 1)
    word.add_word("screwdriver", 1, 2)


@pytest.fixture()
def clean_up_db():
    clean_up()


def clean_up():
    with closing(sqlite3.connect(db.db())) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("DELETE FROM session")
            cursor.execute("DELETE FROM word")
            cursor.execute("DELETE FROM word_comment")
            cursor.execute("DELETE FROM word_multichoice")
            cursor.execute("DELETE FROM word_multichoice_vote")
            cursor.execute("DELETE FROM word_vote")
            connection.commit()


@pytest.fixture(scope="session", autouse=True)
def run_before_all_tests():
    clean_up()

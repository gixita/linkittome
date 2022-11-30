import pytest
import session
import word
import db


@pytest.fixture()
def setup_db_examples():
    session.add_session('2', '3', '4', 1)
    word.add_word("screw", 1, 1)


@pytest.fixture()
def clean_up_db():
    clean_up()


def clean_up():
    db.execute("DELETE FROM session")
    db.execute("DELETE FROM word")
    db.execute("DELETE FROM word_comment")
    db.execute("DELETE FROM word_multichoice")
    db.execute("DELETE FROM word_multichoice_vote")
    db.execute("DELETE FROM word_vote")


@pytest.fixture(scope="session", autouse=True)
def run_before_all_tests():
    clean_up()

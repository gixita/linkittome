from src.storage import db
import sqlite3
from contextlib import closing


def add_word(word: str, session_id: int, ordering: int) -> None:
    """
    Add a new word to the session

    :param word: string of one of the word of the session
    :param session_id: integer representing the unique id of the session (not the PK)
    :param ordering: integer representing the order in which the words are displayed
    """
    with closing(sqlite3.connect(db.db())) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("INSERT INTO  word (word,session_id,ordering) VALUES (?, ?, ?)",
                           (word, session_id, ordering, ))
            connection.commit()


def update_word(word_id: int, word: str, ordering: int) -> None:
    """
    See 'add_word' method for params definition

    :param word_id: primary key of the table word
    :param word: string of one of the word of the session
    :param ordering: integer representing the order in which the words are displayed
    """
    if word is None or word_id < 0:
        raise ValueError("Data incorrect")
    with closing(sqlite3.connect(db.db())) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("UPDATE word SET word = ?, ordering = ? WHERE id = ?",
                           (word, ordering, word_id,))
            connection.commit()


def get_word(word_id: int) -> dict[str, any]:
    """
    Return a dict of the word data with the following keys :
    - 'word': the string of the word
    - 'session_id': the session unique id (not pk)
    - 'ordering': the order of the word for display
    """
    with closing(sqlite3.connect(db.db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            return cursor.execute("SELECT word, session_id, ordering FROM word WHERE id= ? LIMIT 1",
                                  (word_id,)).fetchone()


def delete_word(word_id: int) -> None:
    """
    Delete from the database the word with the primary key word_id
    """
    if word_id < 0:
        raise ValueError("An id cannot be negative")
    with closing(sqlite3.connect(db.db())) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("DELETE FROM word WHERE id = ?",
                           (word_id,))
            connection.commit()


def count_words_in_session(session_id: int) -> int:
    """
    Return the number of words that are linked to the session primary key 'session_id'
    """
    if session_id < 0:
        raise ValueError("An id cannot be negative")
    with closing(sqlite3.connect(db.db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            return cursor.execute("SELECT COUNT(*) as count FROM word WHERE session_id = ?",
                                  (session_id,)).fetchone()['count']


def get_all_words(session_id: int) -> list[dict[str, any]]:
    """
    Return a list of dict with the same keys as the method 'get_word'

    :param session_id: integer primary key of the session table
    :return: a list of dict[str, any] with the keys "word", "session_id" and "ordering"
    """
    # TODO
    if session_id < 0:
        raise ValueError("An id cannot be negative")
    with closing(sqlite3.connect(db.db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            return cursor.execute("SELECT word, session_id, ordering FROM word WHERE session_id = ?", (session_id,))\
                .fetchall()

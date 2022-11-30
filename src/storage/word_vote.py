from src.storage import db
import sqlite3
from contextlib import closing


def add_word_vote(word_id: int, vote: int, vote_text: str) -> None:
    """
    Add a vote linked to a word in the database

    :param word_id: the primary key of the word
    :param vote: integer representing the user vote for the vote
    :param vote_text: a string that can be added to a vote
    """
    if word_id < 0:
        raise ValueError("An id cannot be negative")
    with closing(sqlite3.connect(db.db())) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("INSERT INTO  word_vote (word_id,vote,vote_text) VALUES (?, ?, ?)",
                           (word_id, vote, vote_text, ))
            connection.commit()


def update_word_vote(vote_id: int, vote: int, vote_text: str) -> None:
    """
    Update a word based on the primary key of the vote table

    :param vote_id: primary key of the table word_vote
    :param vote: integer representing the user vote for the vote
    :param vote_text: a string that can be added to a vote
    """
    if vote_id < 0:
        raise ValueError("An id cannot be negative")
    with closing(sqlite3.connect(db.db())) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("UPDATE word_vote SET vote = ?, vote_text = ? WHERE id = ?",
                           (vote, vote_text, vote_id, ))
            connection.commit()


def get_word_vote(vote_id: int) -> dict[str, any]:
    """
    Retrieve a dict containing the vote with the vote primary key 'vote_id'.
    The dict contains the following keys
    - 'word_id' the primary key of the word
    - 'vote' integer representing the user vote for the vote
    - 'vote_text' a string that can be added to a vote
    """
    if vote_id < 0:
        raise ValueError("An id cannot be negative")
    with closing(sqlite3.connect(db.db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            return cursor.execute("SELECT word_id, vote, vote_text FROM word_vote WHERE id= ? LIMIT 1",
                                  (vote_id,)).fetchone()


def get_all_votes_for_word(word_id: int) -> list[dict[str, any]]:
    """
    Retrieve a list of dict containing the votes linked to 'word_id' the primary key of the table word
    The dict contains the following keys
    - 'word_id' the primary key of the word
    - 'vote' integer representing the user vote for the vote
    - 'vote_text' a string that can be added to a vote
    """
    if word_id < 0:
        raise ValueError("An id cannot be negative")
    with closing(sqlite3.connect(db.db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            return cursor.execute("SELECT word_id, vote, vote_text FROM word_vote WHERE word_id= ?", (word_id,))\
                .fetchall()


def delete_word_vote(vote_id: int) -> None:
    """
    Delete the vote based on its primary key 'vote_id'

    :param vote_id: primary key of the vote table
    """
    if vote_id < 0:
        raise ValueError("An id cannot be negative")
    with closing(sqlite3.connect(db.db())) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("DELETE FROM word_vote WHERE id = ?",
                           (vote_id, ))
            connection.commit()

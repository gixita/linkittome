from src.storage import db


def add_word(word: str, session_id: int, ordering: int):
    """
    Add a new word to the session

    :param word: string of one of the word of the session
    :param session_id: integer representing the unique id of the session (not the PK)
    :param ordering: integer representing the order in which the words are displayed
    """
    if word is None or session_id < 0:
        raise ValueError("Data incorrect")
    command = f"INSERT INTO  word (word,session_id,ordering) VALUES ('{word}', {session_id}, {ordering})"
    db.execute(command)


def update_word(word_id: int, word: str, ordering: int):
    """
    See 'add_word' method for params definition

    :param word_id: primary key of the table word
    """
    if word is None or word_id < 0:
        raise ValueError("Data incorrect")
    command = f"UPDATE word SET word = '{word}', ordering = {ordering} WHERE id = {word_id}"
    db.execute(command)


def get_word(word_id: int) -> dict[str, any]:
    """
    Return a dict of the word data with the following keys :
    - 'word': the string of the word
    - 'session_id': the session unique id (not pk)
    - 'ordering': the order of the word for display
    """
    if word_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"SELECT word, session_id, ordering FROM word WHERE id= {word_id} LIMIT 1"
    return db.db_fetchone(command)


def delete_word(word_id: int):
    """
    Delete from the database the word with the primary key word_id
    """
    if word_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"DELETE FROM word WHERE id = {word_id}"
    db.execute(command)


def count_words_in_session(session_id: int) -> int:
    """
    Return the number of words that are linked to the session primary key 'session_id'
    """
    if session_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"SELECT COUNT(*) as count FROM word WHERE session_id = {session_id}"
    return db.db_fetchone(command)['count']


def get_all_words(session_id: int) -> list[dict[str, any]]:
    """
    Return a list of dict with the same keys as the method 'get_word'
    """
    if session_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"SELECT word, session_id, ordering FROM word WHERE session_id = {session_id}"
    return db.db_fetchall(command)

import db


def add_word(word: str, session_id: int, ordering: int):
    if word is None or session_id < 0:
        raise ValueError("Data incorrect")
    command = f"INSERT INTO  word (word,session_id,ordering) VALUES ('{word}', {session_id}, {ordering})"
    db.execute(command)


def update_word(word_id: int, word: str, ordering: int):
    if word is None or word_id < 0:
        raise ValueError("Data incorrect")
    command = f"UPDATE word SET word = '{word}', ordering = {ordering} WHERE id = {word_id}"
    db.execute(command)


def get_word(word_id: int):
    if word_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"SELECT * FROM word WHERE id= {word_id} LIMIT 1"
    return db.db_fetchone(command)


def delete_word(word_id: int):
    if word_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"DELETE FROM word WHERE id = {word_id}"
    db.execute(command)


def count_words_in_session(session_id: int) -> int:
    if session_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"SELECT COUNT(*) as count FROM word WHERE session_id = {session_id}"
    return db.db_fetchone(command)['count']



def get_all_words(session_id: int):
    if session_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"SELECT * FROM word WHERE session_id = {session_id}"
    return db.db_fetchall(command)

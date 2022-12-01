from src.storage import db
import sqlite3
from contextlib import closing


def session_lifetime(s_lifetime: int) -> str:
    f"""
    Create and return a string understood by SQLite to create a date in the future of a specific number of days

    :param s_lifetime: number of days in the future before the session expire
    """
    return f"+{s_lifetime} days"


# Create new session
def add_session(s_uuid: str, c_uuid: str, v_uuid: str, t_id: int, s_lifetime: int):
    f"""
    Store the session in the SQLite database
    
    :param s_uuid: session unique id that allow user to retrieve the session on which they are playing
    :param c_uuid: creator unique id that act as a token for the creator to allow modification of the session
    :param v_uuid: verifier unique id that let the user vote on the word
    :param t_id: type of session, for example all words together or one word at the time
    :param s_lifetime: number of days before the expiration of the session
    and words inside
    """
    with closing(sqlite3.connect(db.db())) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("INSERT INTO session (uuid,type_id,domain_id,verifier_token, creator_token, expiration_date)"
                           " VALUES (?, ?, ?, ?, ?, date('now', ?))",
                           (s_uuid, t_id, 1, v_uuid, c_uuid, session_lifetime(s_lifetime),))
            connection.commit()


def update_session(s_id: int, t_id: int, s_lifetime: int) -> None:
    """
    Update the session in the SQLite database

    :param s_id: session primary key in the database (different from the uuid)
    :param t_id: primary key of the type of session
    :param s_lifetime: number of days before the expiration of the session
    and words inside
    """
    if s_id < 0 or t_id < 0:
        raise ValueError("An id cannot be negative")
    with closing(sqlite3.connect(db.db())) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("UPDATE session SET type_id = ?, expiration_date = date('now', ?) WHERE id = ?",
                           (t_id, session_lifetime(s_lifetime), s_id,))
            connection.commit()


def get_session_by_id(s_id: int) -> dict[str, any]:
    """
    Retrieve session columns as a dict of the session that match the session primary key id

    Keys in the returned dict

    - 'id' primary key of the session
    - 'uuid' unique identifier that allow the user to retrieve the session
    - 'type_id' primary key of the session type
    - 'domain_id' primary key of the mail domain creating a session (can be null)
    - 'verifier_token' the uuid allowing users to vote for the session
    - 'creator_token' the uuid allowing the creator of the session to modify the session type and the words

    :param s_id: primary key of the session
    :return: dict[str, any] with the session
    """
    with closing(sqlite3.connect(db.db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            return cursor.execute("SELECT * FROM session WHERE id=? LIMIT 1", (s_id,)).fetchone()


def get_session_by_uuid(s_uuid: str) -> dict[str, any]:
    """
    Retrieve session columns as a dict of the session that match the session unique id s_uuid
    If the session unique id would appear multiple time in the database, this method would only send one

    Keys in the returned dict

    - 'id' primary key of the session
    - 'uuid' unique identifier that allow the user to retrieve the session
    - 'type_id' primary key of the session type
    - 'domain_id' primary key of the mail domain creating a session (can be null)
    - 'verifier_token' the uuid allowing users to vote for the session
    - 'creator_token' the uuid allowing the creator of the session to modify the session type and the words

    :param s_uuid: string representing the session unique identifier
    :return: dict[str, any] with the session
    """
    with closing(sqlite3.connect(db.db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            return cursor.execute("SELECT * FROM session WHERE uuid=? LIMIT 1", (s_uuid,)).fetchone()


def get_type_id_from_type(type_value: str) -> dict[str, any]:
    """
    Retrieve columns 'id' and 'type' as a dict for the session type that match the string 'type_value'
    It will only return one value even if that value would be entered multiple times

    Example of value in the database:
    id=1; type="all_words_together"


    :param type_value: The string value of the session type
    :return: A dict with the keys id and type
    """
    with closing(sqlite3.connect(db.db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            return cursor.execute("SELECT id, type FROM session_type WHERE type=? LIMIT 1", (type_value,)).fetchone()


def type_id_exists(type_id: int) -> bool:
    """
    Return true if type_id is an existing primary key of the table session_type in the db, return false otherwise

    :param type_id: integer representing the primary key of the table type
    """
    with closing(sqlite3.connect(db.db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            return True if cursor.execute("SELECT COUNT(*) as count FROM session_type WHERE id = ?",
                                          (type_id,)).fetchone()['count'] > 0 else False


def session_id_exists(session_id: int) -> bool:
    """
    Return true if session_id is an existing primary key of the table session in the db, return false otherwise

    :param session_id: integer representing the primary key of the table session
    """
    with closing(sqlite3.connect(db.db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            return True if cursor.execute("SELECT COUNT(*) as count FROM session WHERE id = ?",
                                          (session_id,)).fetchone()['count'] > 0 else False


def session_uuid_exists(session_uuid: str) -> bool:
    """
    Return true if session_id is an existing primary key of the table session in the db, return false otherwise

    :param session_uuid: the unique identifier of the session allowing the user to retrieve it (not the primary key)
    """
    with closing(sqlite3.connect(db.db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            return True if cursor.execute("SELECT COUNT(*) as count FROM session WHERE uuid = ?",
                                          (session_uuid,)).fetchone()['count'] > 0 else False


def get_session_id_from_uuid(session_uuid: str) -> int:
    """
    Return the id of the session uuid

    :param session_uuid: the unique identifier of the session allowing the user to retrieve it (not the primary key)
    :return: integer primary key of the session table
    """
    with closing(sqlite3.connect(db.db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            data = cursor.execute("SELECT id FROM session WHERE uuid = ?", (session_uuid,)).fetchone()
            return data['id'] if data is not None else None


def get_all_types() -> list[dict[str, any]]:
    """
    Return a list containing dict of the types of sessions available.
    The dict will contain the following keys
    - 'id' the primary key of the table session_type
    - 'type' the text representing the type of the session
    """
    with closing(sqlite3.connect(db.db())) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            return cursor.execute("SELECT id, type FROM session_type WHERE 1 ORDER BY id").fetchall()

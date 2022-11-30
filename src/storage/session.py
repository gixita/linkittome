from src.storage import db


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
    if t_id < 0:
        raise ValueError("An id cannot be negative")
    if s_uuid is None or c_uuid is None or v_uuid is None or s_uuid == "" or c_uuid == "" or v_uuid == "":
        raise ValueError("The UUID cannot be empty")
    command = "INSERT INTO session (uuid,type_id,domain_id,verifier_token, creator_token, expiration_date) " \
              f"VALUES ('{s_uuid}',{t_id},{1},'{v_uuid}','{c_uuid}'," \
              f"date('now', '{session_lifetime(s_lifetime)}'))"
    db.execute(command)


def update_session(s_id: int, t_id: int, s_lifetime: int):
    f"""
    For params definition, please refer to the method add_session
    """
    if s_id < 0 or t_id < 0:
        raise ValueError("An id cannot be negative")
    command = "UPDATE session SET " \
              f"type_id = {t_id}, " \
              f"expiration_date = date('now', '{session_lifetime(s_lifetime)}') " \
              f"WHERE id = {s_id}"
    db.execute(command)


# Get new session
def get_session(s_uuid: str):
    f"""
    Retrieve session columns as a dict of the session that match the session unique id 's_uuid'.
    If the session unique id would appear multiple time in the database, this method would only send one

    :param s_uuid: string representing the session unique identifier
    """
    if s_uuid is None or s_uuid == "":
        raise ValueError("The UUID cannot be empty")
    command = f"SELECT * FROM session WHERE uuid='{s_uuid}' LIMIT 1"
    return db.db_fetchone(command)


def get_type_id_from_type(type_value: str) -> dict[str, any]:
    f"""
    Retrieve columns 'id' and 'type' as a dict for the session type that match the string 'type_value'
    It will only return one value even if that value would be entered multiple times

    :param type_value: The string value of the session type
    """
    if type_value == "":
        raise ValueError("Type cannot be empty")
    command = f"SELECT id, type FROM type WHERE type='{type_value}' LIMIT 1"
    return db.db_fetchone(command)


def type_id_exists(type_id: int) -> bool:
    """
    Return true if type_id is an existing primary key of the table type in the db, return false otherwise

    :param type_id: integer representing the primary key of the table type
    """
    if type_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"SELECT COUNT(*) as count FROM session_type WHERE id = {type_id}"
    return True if db.db_fetchone(command)['count'] > 0 else False

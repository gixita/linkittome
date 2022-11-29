import db


def session_lifetime() -> str:
    return '+3 days'


# Create new session
def add_session(s_uuid: str, c_uuid: str, v_uuid: str, t_id: int):
    if t_id < 0:
        raise ValueError("An id cannot be negative")
    if s_uuid is None or c_uuid is None or v_uuid is None or s_uuid == "" or c_uuid == "" or v_uuid == "":
        raise ValueError("The UUID cannot be empty")
    command = "INSERT INTO session (uuid,type_id,domain_id,verifier_token, creator_token, expiration_date) " \
              f"VALUES ('{s_uuid}',{t_id},{1},'{v_uuid}','{c_uuid}'," \
              f"date('now', '{session_lifetime()}'))"
    db.execute(command)


def update_session(s_id: int, t_id: int):
    if s_id < 0 or t_id < 0:
        raise ValueError("An id cannot be negative")
    command = "UPDATE session SET " \
              f"type_id = {t_id}, " \
              f"expiration_date = date('now', '{session_lifetime()}') " \
              f"WHERE id = {s_id}"
    db.execute(command)


# Get new session
def get_session(s_uuid: str):
    if s_uuid is None or s_uuid == "":
        raise ValueError("The UUID cannot be empty")
    command = f"SELECT * FROM session WHERE uuid='{s_uuid}' LIMIT 1"
    return db.db_fetchone(command)

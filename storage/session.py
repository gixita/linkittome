import db


def session_lifetime() -> str:
    return '+3 days'


# Create new session
def add_session(s_uuid: str, c_uuid: str, v_uuid: str, t_id: int):
    command = "INSERT INTO session (uuid,type_id,domain_id,verifier_token, creator_token, expiration_date) " \
                        "VALUES ('" + s_uuid + "'," + str(t_id) + "," + str(1) + ",'" + v_uuid + "','" + c_uuid + \
                        "',date('now', '" + session_lifetime() + "'))"
    db.execute(command)


# Get new session
def get_session(s_uuid: str):
    command = "SELECT * FROM session WHERE session_uuid='"+s_uuid+"'"
    db.db_fetchone(command)

import uuid
from src.storage import session


def session_lifetime(days=3) -> int:
    """
    Represent the number of days starting now when the session should expire
    """
    if days <= 0:
        raise ValueError("The expiration timeframe in days cannot be zero or negative")
    return days


def type_id_exists(type_id: int) -> bool:
    """
    Return true is the type identifier exists in the database
    """
    if type_id < 0:
        raise IndexError("Type id cannot be negative")
    return session.type_id_exists(type_id)


def get_all_types():
    """
    API facing function
    Return all types available in a list of dict containing the keys
    - 'id'
    - 'type'
    """
    return session.get_all_types()


def session_id_exists(session_id: int) -> bool:
    """
    Return true is the session identifier exists in the database
    """
    if session_id < 0:
        raise IndexError("Type id cannot be negative")
    if not isinstance(session_id, int):
        raise TypeError("Session identifier should be an integer")
    return session.session_id_exists(session_id)


def create_session(type_id: int, days=3):
    """
    API facing function
    Create a new session by defining a type.
    The primary key 'type_id' needs to exist in the database otherwise it will throw an IndexError error

    :param type_id: primary key of the type id
    :param days: number of days before the expiration of the session
    """
    session_uuid = str(uuid.uuid4())
    creator_uuid = str(uuid.uuid4())
    verifiers_uuid = str(uuid.uuid4())
    if not isinstance(type_id, int):
        raise TypeError("The type_id should be an int")
    if not isinstance(days, int):
        raise TypeError("The days should be an int")
    if type_id < 0:
        raise IndexError("The type id should not be negative")
    if days < 0:
        raise ValueError("The number of days after which the session will expire cannot be negative")
    if not type_id_exists(type_id):
        raise IndexError("Type id is not existing in the database")
    session.add_session(session_uuid, creator_uuid, verifiers_uuid, type_id, session_lifetime(days))
    return {'session_uuid': session_uuid,
            'creator_uuid': creator_uuid,
            'verifiers_uuid': verifiers_uuid,
            'type_id': type_id}


def update_session(session_id: int, type_id: int, s_lifetime: int) -> None:
    """
    API facing function
    Update an existing function. The session, creator and verifier uuid are immutable and so cannot be modified.

    :param session_id: session primary key in the database (different from the uuid)
    :param type_id: primary key of the type of session
    :param s_lifetime: number of days before the expiration of the session
    """
    if not isinstance(type_id, int) or not isinstance(session_id, int) or isinstance(s_lifetime, int):
        raise TypeError("The argument should be an int")
    if type_id < 0:
        raise IndexError("The type id should not be negative")
    if session_id < 0:
        raise IndexError("The session id should not be negative")
    if s_lifetime < 0:
        raise IndexError("The number of days after which the session will expire cannot be negative")
    if not type_id_exists(type_id):
        raise IndexError("Type id is not existing in the database")
    session.update_session(session_id, type_id, s_lifetime)


def get_session(session_uuid: str) -> dict[str, any]:
    """
    Retrieve session columns as a dict of the session that match the session unique id s_uuid
    If the session unique id would appear multiple time in the database, this method would only send one

    The returned dict contains the following keys

    - 'id' primary key of the session
    - 'uuid' unique identifier that allow the user to retrieve the session
    - 'type_id' primary key of the session type
    - 'domain_id' primary key of the mail domain creating a session (can be null)
    - 'verifier_token' the uuid allowing users to vote for the session
    - 'creator_token' the uuid allowing the creator of the session to modify the session type and the words

    :param session_uuid: string representing the session unique identifier
    """
    if not isinstance(session_uuid, str):
        raise TypeError("The argument should be an int")
    if session_uuid is "":
        raise ValueError("The session uuid should not be empty")
    if not session.session_uuid_exists(session_uuid):
        raise IndexError("The session do not exist in the database")
    return session.get_session(session_uuid)


def get_type_id_from_type(type_value: str) -> dict[str, any]:
    """
    Retrieve the session type as a dict that match the string 'type_value'
    It will only return one value even if that value would be entered multiple times

    The dict keys are:

    - 'id' primary key of the session type
    - 'type' the string representing the type

    :param type_value: The string value of the session type
    """

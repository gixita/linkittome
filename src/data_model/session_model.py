import uuid
from src.storage import session


def session_lifetime(days=3) -> int:
    """
    Represent the number of days starting now when the session should expire
    """
    if days <= 0:
        raise ValueError("The expiration timeframe in days cannot be zero or negative")
    return days


def add_session(type_id: int, days=3):
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

    :raises IndexError session_id: The session id should not be negative
    :raises IndexError type_id: The type id should not be negative
    :param session_id: session primary key in the database (different from the uuid)
    :param type_id: primary key of the type of session
    :param s_lifetime: number of days before the expiration of the session
    """
    if not isinstance(session_id, int) or not isinstance(type_id, int) or not isinstance(s_lifetime, int):
        raise TypeError("The argument should be an int")
    if session_id < 0:
        raise IndexError("The session id must be positive")
    if type_id < 0:
        raise IndexError("The type id must be positive")
    if s_lifetime < 0:
        raise IndexError("The number of days after which the session will expire cannot be negative")
    if not session_id_exists(session_id):
        raise IndexError("Session id is not existing in the database")
    if not type_id_exists(type_id):
        raise IndexError("Type id is not existing in the database")
    session.update_session(session_id, type_id, s_lifetime)


def get_session_by_id(session_id: int) -> dict[str, any]:
    """
    Retrieve session columns as a dict of the session that match the session primary key id

    The returned dict contains the following keys

    - 'id' primary key of the session
    - 'uuid' unique identifier that allow the user to retrieve the session
    - 'type_id' primary key of the session type
    - 'domain_id' primary key of the mail domain creating a session (can be null)
    - 'verifier_token' the uuid allowing users to vote for the session
    - 'creator_token' the uuid allowing the creator of the session to modify the session type and the words

    :param session_id: primary key of the session
    :return: dict[str, any] with the session
    """
    if not isinstance(session_id, int):
        raise TypeError("The session id should be an int")
    if session_id < 0:
        raise IndexError("The session id must be positive")
    data = session.get_session_by_id(session_id)
    if data is None:
        raise IndexError("The session primary key don't exist in the database")
    return data


def get_session_by_uuid(session_uuid: str) -> dict[str, any]:
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
        raise TypeError("The argument should be an string")
    if session_uuid is "":
        raise ValueError("The session uuid should not be empty")
    if not session.session_uuid_exists(session_uuid):
        raise IndexError("The session do not exist in the database")
    return session.get_session_by_uuid(session_uuid)


def get_type_id_from_type(type_value: str) -> dict[str, any]:
    """
    Retrieve the session type as a dict that match the string 'type_value'
    It will only return one value even if that value would be entered multiple times

    The dict keys are:

    - 'id' primary key of the session type
    - 'type' the string representing the type

    :param type_value: The string value of the session type
    :return: dict[str, any] containing the "id" and "type" of the session type. One type for example
    is "all_words_together"
    """
    if not isinstance(type_value, str):
        raise TypeError("Type value should be a string")
    if type_value == "" or type_value is None:
        raise ValueError("Type cannot be empty")
    data = session.get_type_id_from_type(type_value)
    if data is None:
        raise IndexError("Type value do not exist in the database")
    return data


def type_id_exists(type_id: int) -> bool:
    """
    Check if the type identifier exists in the database

    :return: boolean, true is the type identifier exists in the database, false otherwise
    """

    if not isinstance(type_id, int):
        raise TypeError("Type id should be a integer")
    if type_id < 0:
        raise IndexError("Type id cannot be negative")
    return session.type_id_exists(type_id)


def session_id_exists(session_id: int) -> bool:
    """
    Check if the session identifier exists in the database

    :return: boolean true if the session identifier exists in the database
    """
    if not isinstance(session_id, int):
        raise TypeError("Session identifier should be an integer")
    if session_id < 0:
        raise IndexError("Session id cannot be negative")
    return session.session_id_exists(session_id)


def session_uuid_exists(session_uuid: str) -> bool:
    """
    Return true if session_id is an existing primary key of the table session in the db, return false otherwise

    :param session_uuid: the unique identifier of the session allowing the user to retrieve it (not the primary key)
    """
    if not isinstance(session_uuid, str):
        raise TypeError("Session unique identifier should be a string")
    if session_uuid == "" or session_uuid is None:
        raise ValueError("Session unique identifier cannot be empty")
    return session.session_uuid_exists(session_uuid)


def get_session_id_from_uuid(session_uuid: str) -> int:
    """
    Get the session primary key from the unique identifier of the session

    :param session_uuid: String of the unique identifier of the session
    :return: integer primary key of the table session
    """
    if not isinstance(session_uuid, str):
        raise TypeError("Session unique identifier should be a string")
    if session_uuid == "" or session_uuid is None:
        raise ValueError("Session unique identifier cannot be empty")
    data = session.get_session_id_from_uuid(session_uuid)
    if data is None:
        raise IndexError("Session uuid do not exist in the database")
    return session.get_session_id_from_uuid(session_uuid)


def get_all_types() -> list[dict[str, any]]:
    """
    API facing function

    Return all types available in a list of dict containing the keys

    :return: list of dict[str, any] containing the "id" and "type" keys
    """
    return session.get_all_types()

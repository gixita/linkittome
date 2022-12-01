from src.data_model import session_model
from src.storage import word


def add_word(word_value: str, session_id: int, ordering: int) -> None:
    """
    Add a new word linked to a session
    :param word_value: string of one of the word of the session
    :param session_id: integer representing the unique id of the session (not the PK)
    :param ordering: integer representing the order in which the words are displayed
    """
    if not isinstance(word_value, str) or not isinstance(session_id, int) or not isinstance(ordering, int):
        raise TypeError("One of the argument has an incorrect type")
    if word_value is "" or word_value is None:
        raise ValueError("Word cannot be empty or null")
    if session_id < 0:
        raise IndexError("The session ID cannot be negative")
    if not session_model.session_id_exists(session_id):
        raise IndexError("Session id do not exists in the database")
    word.add_word(word_value, session_id, ordering)


def get_word_by_id(word_id: int) -> dict[str, any]:
    """
    Return a dict of the word data with the following keys :
    - 'word': the string of the word
    - 'session_id': the session unique id (not pk)
    - 'ordering': the order of the word for display
    """
    if not isinstance(word_id, int):
        raise TypeError("One of the argument has an incorrect type")
    if word_id < 0:
        raise ValueError("An id cannot be negative")
    data = word.get_word(word_id)
    if data is None:
        raise IndexError("Word id is not existing in the database")
    return data

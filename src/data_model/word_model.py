from src.data_model import session_model

def add_word(word: str, session_id: int, ordering: int):
    """
    Add a new word linked to a session
    :param word: string of one of the word of the session
    :param session_id: integer representing the unique id of the session (not the PK)
    :param ordering: integer representing the order in which the words are displayed
    """
    if word is "" or word is None:
        raise ValueError("Word cannot be empty or null")

    if session_id < 0:
        raise IndexError("The session ID cannot be negative")

    if word is not str or session_id is not int or ordering is not int:
        raise TypeError("One of the argument has an incorrect type")

    if not session_model.session_id_exists(session_id):
        raise IndexError("Session id do not exists in the database")


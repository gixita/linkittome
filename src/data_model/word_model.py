from src.data_model import session_model
from src.storage import word


def quality_check_word_id(word_id: int, disable_exists_check=False) -> None:
    if not isinstance(word_id, int):
        raise TypeError("word_id argument has an incorrect type")
    if word_id < 0:
        raise IndexError("The word ID cannot be negative")
    if not disable_exists_check:
        if not word_id_exists(word_id):
            raise IndexError("Word id do not exists in the database")


def quality_check_word_value(word_value: str) -> None:
    if not isinstance(word_value, str):
        raise TypeError("word_value argument has an incorrect type")
    if word_value is "" or word_value is None:
        raise ValueError("Word cannot be empty or null")


def quality_check_session_id(session_id: int, disable_exists_check=False) -> None:
    if not isinstance(session_id, int):
        raise TypeError("One of the argument has an incorrect type")
    if session_id < 0:
        raise IndexError("The session ID cannot be negative")
    if not disable_exists_check:
        if not session_model.session_id_exists(session_id):
            raise IndexError("Session id do not exists in the database")


def quality_check_ordering(ordering: int) -> None:
    if not isinstance(ordering, int):
        raise TypeError("Ordering argument has an incorrect type")


def add_word(word_value: str, session_id: int, ordering: int) -> None:
    """
    Add a new word linked to a session
    :param word_value: string of one of the word of the session
    :param session_id: integer representing the unique id of the session (not the PK)
    :param ordering: integer representing the order in which the words are displayed
    """
    quality_check_word_value(word_value)
    quality_check_session_id(session_id)
    quality_check_ordering(ordering)
    word.add_word(word_value, session_id, ordering)


def update_word(word_id: int, word_value: str, ordering: int) -> None:
    """
    Update the word in the database

    :param word_id: primary key of the table word
    :param word_value: string of one of the word of the session
    :param ordering: integer representing the order in which the words are displayed
    """
    quality_check_word_id(word_id)
    quality_check_word_value(word_value)
    quality_check_ordering(ordering)
    word.update_word(word_id, word_value, ordering)


def get_word_by_id(word_id: int) -> dict[str, any]:
    """
    Return a dict of the word data with the following keys :
    - 'word': the string of the word
    - 'session_id': the session unique id (not pk)
    - 'ordering': the order of the word for display
    """
    quality_check_word_id(word_id)
    return word.get_word(word_id)


def word_id_exists(word_id: int) -> bool:
    """
    Check if the word primary key exists

    :param word_id: integer primary key of the word table
    :return: boolean, true if exists
    """
    quality_check_word_id(word_id, True)
    return word.word_id_exists(word_id)


def delete_word(word_id: int) -> None:
    """
    Delete the word with the primary key word_id
    """
    quality_check_word_id(word_id)
    word.delete_word(word_id)


def count_words_in_session(session_id: int) -> int:
    """
    Return the number of words that are linked to the session primary key 'session_id'
    """

    quality_check_session_id(session_id)
    return word.count_words_in_session(session_id)


def get_all_words(session_id: int) -> list[dict[str, any]]:
    """
    Return a list of dict with the same keys as the method 'get_word'

    :param session_id: integer primary key of the session table
    :return: a list of dict[str, any] with the keys "id", "word", "session_id" and "ordering"
    """
    quality_check_session_id(session_id)
    return word.get_all_words(session_id)

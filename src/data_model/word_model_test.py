import pytest
from src.data_model import word_model


# noinspection PyTypeChecker
def test_add_word_wrong_type_word():
    with pytest.raises(TypeError, match="One of the argument has an incorrect type"):
        word_model.add_word(1, 1, 1)


# noinspection PyTypeChecker
def test_add_word_wrong_type_session():
    with pytest.raises(TypeError, match="One of the argument has an incorrect type"):
        word_model.add_word("test", "", 1)


# noinspection PyTypeChecker
def test_add_word_wrong_type_ordering():
    with pytest.raises(TypeError, match="One of the argument has an incorrect type"):
        word_model.add_word("test", 1, "")


def test_add_word_word_empty():
    with pytest.raises(ValueError, match="Word cannot be empty or null"):
        word_model.add_word("", 1, 1)


def test_add_word_session_negative():
    with pytest.raises(IndexError, match="The session ID cannot be negative"):
        word_model.add_word("test", -99, 1)


def test_add_word_session_unknown(clean_up_db, setup_db_examples):
    with pytest.raises(IndexError, match="Session id do not exists in the database"):
        word_model.add_word("test", 99, 1)


def test_add_word(clean_up_db, setup_db_examples):
    word_model.add_word('rose', 1, 0)
    data = word_model.get_word_by_id(3)
    assert data is not None
    assert data['word'] == "rose"

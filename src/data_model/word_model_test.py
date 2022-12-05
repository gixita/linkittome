import pytest
from src.data_model import word_model


# noinspection PyTypeChecker
def quality_check_word_id_wrong_type():
    with pytest.raises(TypeError, match="word_id argument has an incorrect type"):
        word_model.quality_check_word_id("")


def quality_check_word_id_negative():
    with pytest.raises(IndexError, match="The word ID cannot be negative"):
        word_model.quality_check_word_id(-1)


def quality_check_word_id_unknown():
    with pytest.raises(IndexError, match="Word id do not exists in the database"):
        word_model.quality_check_word_id(99)


# noinspection PyTypeChecker
def test_quality_check_word_value_wrong_type():
    with pytest.raises(TypeError, match="word_value argument has an incorrect type"):
        word_model.quality_check_word_value(1)


def quality_check_word_value_empty():
    with pytest.raises(ValueError, match="Word cannot be empty or null"):
        word_model.quality_check_word_value("")


# noinspection PyTypeChecker
def quality_check_session_id_wrong_type():
    with pytest.raises(TypeError, match="One of the argument has an incorrect type"):
        word_model.quality_check_session_id("")


def quality_check_session_id_negative():
    with pytest.raises(IndexError, match="The session ID cannot be negative"):
        word_model.quality_check_session_id(-1)


def quality_check_session_id_unknown():
    with pytest.raises(IndexError, match="Session id do not exists in the database"):
        word_model.quality_check_session_id(99)


# noinspection PyTypeChecker
def quality_check_ordering_wrong_type():
    with pytest.raises(TypeError, match="Ordering argument has an incorrect type"):
        word_model.quality_check_ordering("")


def test_add_word(clean_up_db, setup_db_examples):
    word_model.add_word('rose', 1, 0)
    data = word_model.get_word_by_id(3)
    assert data is not None
    assert data['word'] == "rose"


def test_update_word(clean_up_db, setup_db_examples):
    word_model.add_word('rose', 1, 0)
    word_model.update_word(3, "New value", 2, 1)
    data = word_model.get_word_by_id(3)
    assert data is not None
    assert data['word'] == "New value"
    assert data['ordering'] == 2


def test_get_word_by_id(clean_up_db, setup_db_examples):
    word_model.add_word('rose', 1, 0)
    data = word_model.get_word_by_id(3)
    assert data is not None
    assert data['word'] == "rose"
    assert data['ordering'] == 0


def test_word_id_exists(clean_up_db, setup_db_examples):
    assert word_model.word_id_exists(1)


def test_delete_word(clean_up_db, setup_db_examples):
    word_model.add_word('rose', 1, 0)
    word_model.delete_word(3, 1)
    assert word_model.count_words_in_session(1) == 2


def test_delete_word_with_wrong_session(clean_up_db, setup_db_examples):
    word_model.add_word('rose', 1, 0)
    with pytest.raises(IndexError, match="The word don't belong to your session"):
        word_model.delete_word(3, 2)
    assert word_model.count_words_in_session(1) == 3


def test_count_words_in_session(clean_up_db, setup_db_examples):
    assert word_model.count_words_in_session(1) == 2


def test_get_all_words(clean_up_db, setup_db_examples):
    data = word_model.get_all_words(1)
    assert len(data) == 2
    assert data[0]['word_id'] == 1
    assert data[0]['word'] == "screw"
    assert data[0]['session_id'] == 1
    assert data[0]['ordering'] == 1

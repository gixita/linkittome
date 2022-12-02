from src.data_model import word_vote_model
import pytest


# noinspection PyTypeChecker
def test_quality_check_vote_id_wrong_type():
    with pytest.raises(TypeError, match="vote_id argument has an incorrect type"):
        word_vote_model.quality_check_vote_id("")


def test_quality_check_vote_id_negative():
    with pytest.raises(IndexError, match="The vote_id cannot be negative"):
        word_vote_model.quality_check_vote_id(-1)


def test_quality_check_vote_id_unknown():
    with pytest.raises(IndexError, match="vote_id do not exists in the database"):
        word_vote_model.quality_check_vote_id(99)


# noinspection PyTypeChecker
def test_quality_check_word_id_wrong_type():
    with pytest.raises(TypeError, match="word_id argument has an incorrect type"):
        word_vote_model.quality_check_word_id("")


def test_quality_check_word_id_negative():
    with pytest.raises(IndexError, match="The word ID cannot be negative"):
        word_vote_model.quality_check_word_id(-1)


def test_quality_check_word_id_unknown():
    with pytest.raises(IndexError, match="Word id do not exists in the database"):
        word_vote_model.quality_check_word_id(99)


# noinspection PyTypeChecker
def test_quality_check_vote_wrong_type():
    with pytest.raises(TypeError, match="vote argument has an incorrect type"):
        word_vote_model.quality_check_vote("")


# noinspection PyTypeChecker
def quality_check_vote_text_wrong_type():
    with pytest.raises(TypeError, match="vote_text argument has an incorrect type"):
        word_vote_model.quality_check_vote_text(1)


def quality_check_vote_text_empty():
    with pytest.raises(ValueError, match="vote_text cannot be empty or null"):
        word_vote_model.quality_check_vote_text_should_not_be_empty("")


def test_add_word_vote(clean_up_db, setup_db_examples):
    word_vote_model.add_word_vote(1, 5, "test", 1)
    data = word_vote_model.get_word_vote(1)
    assert data['id'] == 1
    assert data['word_id'] == 1
    assert data['vote'] == 5
    assert data['vote_text'] == "test"
    # word_vote_model.add_word_vote(1, 0, "test second vote", 1)
    # data = word_vote_model.get_word_vote(2)


def test_update_word_vote(clean_up_db, setup_db_examples):
    word_vote_model.add_word_vote(1, 5, "test", 1)
    word_vote_model.update_word_vote(1, 2, "updated vote", 1)
    data = word_vote_model.get_word_vote(1)
    assert data['id'] == 1
    assert data['word_id'] == 1
    assert data['vote'] == 2
    assert data['vote_text'] == "updated vote"


def test_get_word_vote(clean_up_db, setup_db_examples):
    with pytest.raises(IndexError, match="The vote_id cannot be negative or null"):
        word_vote_model.get_word_vote(0)
    with pytest.raises(IndexError, match="vote_id do not exists in the database"):
        word_vote_model.get_word_vote(99)


def test_get_all_votes_for_word(clean_up_db, setup_db_examples):
    assert len(word_vote_model.get_all_votes_for_word(1)) == 0
    word_vote_model.add_word_vote(1, 5, "test", 1)
    assert len(word_vote_model.get_all_votes_for_word(1)) == 1


def test_delete_word_vote(clean_up_db, setup_db_examples):
    with pytest.raises(IndexError, match="vote_id do not exists in the database"):
        word_vote_model.delete_word_vote(1)
    word_vote_model.add_word_vote(1, 5, "test", 1)
    assert len(word_vote_model.get_all_votes_for_word(1)) == 1


def test_vote_id_exists(clean_up_db, setup_db_examples):
    assert not word_vote_model.vote_id_exists(1)
    word_vote_model.add_word_vote(1, 5, "test", 1)
    assert word_vote_model.vote_id_exists(1)


def test_count_vote_for_word(clean_up_db, setup_db_examples):
    assert 0 == word_vote_model.count_vote_for_word(1)
    word_vote_model.add_word_vote(1, 5, "test", 1)
    assert 1 == word_vote_model.count_vote_for_word(1)

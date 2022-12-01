from src.storage import word


def test_add_word(clean_up_db, setup_db_examples):
    word.add_word("screw", 1, 1)
    data = word.get_word(1)
    assert "screw" == data['word']


def test_update_word():
    word.add_word("screw", 1, 1)
    word.update_word(1, "New screw", 2)
    data = word.get_word(1)
    assert "New screw" == data["word"]
    assert 1 == data["session_id"]
    assert 2 == data["ordering"]


def test_get_word(clean_up_db, setup_db_examples):
    word.add_word("screw", 1, 1)
    data = word.get_word(1)
    assert "screw" == data["word"]
    assert 1 == data["session_id"]
    assert 1 == data["ordering"]


def test_delete_word(clean_up_db, setup_db_examples):
    word.add_word("screw", 1, 1)
    previous_number_of_words = word.count_words_in_session(1)
    word.delete_word(1)
    assert previous_number_of_words > word.count_words_in_session(1)


def test_count_words_in_session(clean_up_db, setup_db_examples):
    word.add_word("screw", 1, 1)
    assert 3 == word.count_words_in_session(1)


def test_get_all_words(clean_up_db, setup_db_examples):
    data = word.get_all_words(1)
    assert len(data) == 2
    assert data[0]['word'] is not None
    assert data[0]['session_id'] is not None
    assert data[0]['ordering'] is not None

from src.storage import word_vote


def test_add_word_vote(clean_up_db, setup_db_examples):
    word_vote.add_word_vote(1, 1, "Nice job")
    data = word_vote.get_word_vote(1)
    assert 1 == data['word_id']
    assert 1 == data['vote']
    assert "Nice job" == data['vote_text']


def test_update_word_vote(clean_up_db, setup_db_examples):
    word_vote.add_word_vote(1, 1, "Nice job")
    data = word_vote.get_word_vote(1)
    word_vote.update_word_vote(1, 2, 'updated vote')
    data1 = word_vote.get_word_vote(1)
    assert 1 == data1['word_id']
    assert 1 == data['vote']
    assert "updated vote" == data1['vote_text']
    assert 2 == data1['vote']


def test_get_word_vote(clean_up_db, setup_db_examples):
    word_vote.add_word_vote(1, 1, "Nice job")
    data = word_vote.get_word_vote(1)
    assert 1 == data['word_id']
    assert 1 == data['vote']
    assert "Nice job" == data['vote_text']


def test_get_all_votes_for_word(clean_up_db, setup_db_examples):
    word_vote.add_word_vote(1, 1, "Nice job")
    word_vote.add_word_vote(1, 2, "Nice job")
    word_vote.add_word_vote(1, 3, "Nice job1")
    data = word_vote.get_all_votes_for_word(1)
    assert 3 == len(data)
    assert 1 == data[0]['vote']


def test_delete_word_vote(clean_up_db, setup_db_examples):
    word_vote.add_word_vote(1, 1, "Nice job")
    word_vote.add_word_vote(1, 2, "Nice job")
    word_vote.add_word_vote(1, 3, "Nice job1")
    word_vote.delete_word_vote(1)
    word_vote.delete_word_vote(2)
    data = word_vote.get_all_votes_for_word(1)
    assert 1 == len(data)
    assert 3 == data[0]['vote']
from src.data_model import word_vote_model
import pytest
from src.errors.rules_errors import OneVotePerWordError


def test_add_word_vote_cannot_add_more_than_one(clean_up_db, setup_db_examples):
    word_vote_model.add_word_vote(1, 5, "test", 1)
    with pytest.raises(OneVotePerWordError):
        word_vote_model.add_word_vote(1, 0, "test second vote", 1)

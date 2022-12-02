from src.data_model import word_model, session_model
from src.storage import word_vote
from src.errors.rules_errors import OneVotePerWordError, ImmutableVoteError


def hardcoded_rules(type_id: int) -> dict[str, bool]:
    """
    Temporary solution to enumerate multiple rules in the future (currently only two rules).
    TODO
    The rules should be part of the session_type table in the future. But the type should have
    dedicated files and tests for it (not linked to the session files)

    :return key one_vote_per_word: boolean, true if only one vote per word is allowed
    :return key everybody_can_vote: boolean, true if everyone can vote with a session token
    :return key all_words_together: boolean, true if all words should be voted on one page
    :return key wait_for_admin: boolean, true if creator unlock new vote manually
    :return key immutable_vote: boolean, true if vote cannot be modified, except by creator
        :return key limit_vote_per_user: boolean, true if the user has a limited amount of votes he can do
    """
    if type_id == 1:
        return {'one_vote_per_word': True,
                'everybody_can_vote': True,
                'all_words_together': True,
                'wait_for_admin': False,
                'immutable_vote': False}
    if type_id == 2:
        return {'one_vote_per_word': True,
                'everybody_can_vote': True,
                'all_words_together': False,
                'wait_for_admin': False,
                'immutable_vote': False}
    if type_id == 3:
        # Fully permissive one
        return {'one_vote_per_word': False,
                'everybody_can_vote': True,
                'all_words_together': True,
                'wait_for_admin': False,
                'immutable_vote': False}


def quality_check_vote_id(vote_id: int, disable_exists_check=False) -> None:
    if not isinstance(vote_id, int):
        raise TypeError("vote_id argument has an incorrect type")
    if vote_id <= 0:
        raise IndexError("The vote_id cannot be negative or null")
    if not disable_exists_check:
        if not vote_id_exists(vote_id):
            raise IndexError("vote_id do not exists in the database")


def quality_check_word_id(word_id: int, disable_exists_check=False) -> None:
    if not isinstance(word_id, int):
        raise TypeError("word_id argument has an incorrect type")
    if word_id < 0:
        raise IndexError("The word ID cannot be negative")
    if not disable_exists_check:
        if not word_model.word_id_exists(word_id):
            raise IndexError("Word id do not exists in the database")


def quality_check_vote(vote: int, disable_exists_check=False) -> None:
    if not isinstance(vote, int):
        raise TypeError("vote argument has an incorrect type")


def quality_check_vote_text(vote_text: str) -> None:
    if not isinstance(vote_text, str):
        raise TypeError("vote_text argument has an incorrect type")


def quality_check_vote_text_should_not_be_empty(vote_text: str) -> None:
    if vote_text is "" or vote_text is None:
        raise ValueError("vote_text cannot be empty or null")


def add_word_vote(word_id: int, vote: int, vote_text: str, session_id: int) -> None:
    """
    Add a vote linked to a word in the database

    :param word_id: the primary key of the word
    :param vote: integer representing the user vote for the vote
    :param vote_text: a string that can be added to a vote
    :param session_id: primary key of the session table
    """
    quality_check_word_id(word_id)
    quality_check_vote(vote)
    quality_check_vote_text(vote_text)
    word_model.quality_check_session_id(session_id)
    rules = hardcoded_rules(session_model.get_session_by_id(session_id)['type_id'])
    if rules['one_vote_per_word']:
        if count_vote_for_word(word_id) > 0:
            raise OneVotePerWordError()
    word_vote.add_word_vote(word_id, vote, vote_text)


def update_word_vote(vote_id: int, vote: int, vote_text: str, session_id: int) -> None:
    """
    Update a word based on the primary key of the vote table

    :param vote_id: primary key of the table word_vote
    :param vote: integer representing the user vote for the vote
    :param vote_text: a string that can be added to a vote
    :param session_id: primary key of the session table
    """
    quality_check_vote_id(vote_id)
    quality_check_vote(vote)
    quality_check_vote_text(vote_text)
    word_model.quality_check_session_id(session_id)
    rules = hardcoded_rules(session_model.get_session_by_id(session_id)['type_id'])
    if rules['immutable_vote']:
        # TODO should check if user is creator and allow it
        raise ImmutableVoteError()
    word_vote.update_word_vote(vote_id, vote, vote_text)


def get_word_vote(vote_id: int) -> dict[str, any]:
    """
    Retrieve a dict containing the vote with the vote primary key 'vote_id'.
    The dict contains the following keys
    - 'id' the primary key of the table word_vote
    - 'word_id' the primary key of the word
    - 'vote' integer representing the user vote for the vote
    - 'vote_text' a string that can be added to a vote
    """
    quality_check_vote_id(vote_id)
    return word_vote.get_word_vote(vote_id)


def get_all_votes_for_word(word_id: int) -> list[dict[str, any]]:
    """
    Retrieve a list of dict containing the votes linked to 'word_id' the primary key of the table word
    The dict contains the following keys
    - 'word_id' the primary key of the word
    - 'vote' integer representing the user vote for the vote
    - 'vote_text' a string that can be added to a vote
    """
    quality_check_word_id(word_id)
    return word_vote.get_all_votes_for_word(word_id)


def delete_word_vote(vote_id: int) -> None:
    """
    Delete the vote based on its primary key 'vote_id'

    :param vote_id: primary key of the vote table
    """
    quality_check_vote_id(vote_id)
    word_vote.delete_word_vote(vote_id)


def vote_id_exists(vote_id: int) -> bool:
    """
    Check if the vote primary key vote_id exists in the database

    :param vote_id: integer primary key of the table word_vote
    :return: boolean, true if the primary key exists
    """
    quality_check_vote_id(vote_id, True)
    return word_vote.vote_id_exists(vote_id)


def count_vote_for_word(word_id: int) -> int:
    quality_check_word_id(word_id)
    return word_vote.count_votes_in_word(word_id)
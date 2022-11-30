from src.storage import db


def add_word_vote(word_id: int, vote: int, vote_text: str) -> None:
    """
    Add a vote linked to a word in the database

    :param word_id: the primary key of the word
    :param vote: integer representing the user vote for the vote
    :param vote_text: a string that can be added to a vote
    """
    if word_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"INSERT INTO  word_vote (word_id,vote,vote_text) VALUES ('{word_id}', {vote}, '{vote_text}')"
    db.execute(command)


def update_word_vote(vote_id: int, vote: int, vote_text: str) -> None:
    """
    Update a word based on the primary key of the vote table

    :param vote_id: primary key of the table word_vote
    :param vote: integer representing the user vote for the vote
    :param vote_text: a string that can be added to a vote
    """
    if vote_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"UPDATE word_vote SET vote = '{vote}', vote_text = '{vote_text}' WHERE id = {vote_id}"
    db.execute(command)


def get_word_vote(vote_id: int) -> dict[str, any]:
    """
    Retrieve a dict containing the vote with the vote primary key 'vote_id'.
    The dict contains the following keys
    - 'word_id' the primary key of the word
    - 'vote' integer representing the user vote for the vote
    - 'vote_text' a string that can be added to a vote
    """
    if vote_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"SELECT word_id, vote, vote_text FROM word_vote WHERE id= {vote_id} LIMIT 1"
    return db.db_fetchone(command)


def get_all_votes_for_word(word_id: int) -> list[dict[str, any]]:
    """
    Retrieve a list of dict containing the votes linked to 'word_id' the primary key of the table word
    The dict contains the following keys
    - 'word_id' the primary key of the word
    - 'vote' integer representing the user vote for the vote
    - 'vote_text' a string that can be added to a vote
    """
    if word_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"SELECT word_id, vote, vote_text FROM word_vote WHERE word_id= {word_id}"
    return db.db_fetchall(command)


def delete_word_vote(vote_id: int) -> None:
    """
    Delete the vote based on its primary key 'vote_id'

    :param vote_id: primary key of the vote table
    """
    if vote_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"DELETE FROM word_vote WHERE id = {vote_id}"
    db.execute(command)

import db


def add_word_vote(word_id: int, vote: int, vote_text: str) -> None:
    if word_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"INSERT INTO  word_vote (word_id,vote,vote_text) VALUES ('{word_id}', {vote}, '{vote_text}')"
    db.execute(command)


def update_word_vote(vote_id: int, vote: int, vote_text: str) -> None:
    if vote_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"UPDATE word_vote SET vote = '{vote}', vote_text = '{vote_text}' WHERE id = {vote_id}"
    db.execute(command)


def get_word_vote(vote_id: int) -> dict[str, any]:
    if vote_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"SELECT * FROM word_vote WHERE id= {vote_id} LIMIT 1"
    return db.db_fetchone(command)


def get_all_votes_for_word(word_id: int) -> list[dict[str, any]]:
    if word_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"SELECT * FROM word_vote WHERE word_id= {word_id}"
    return db.db_fetchall(command)


def delete_word_vote(vote_id: int) -> None:
    if vote_id < 0:
        raise ValueError("An id cannot be negative")
    command = f"DELETE FROM word_vote WHERE id = {vote_id}"
    db.execute(command)

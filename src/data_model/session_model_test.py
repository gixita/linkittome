import pytest
from src.data_model import session_model


def test_session_lifetime():
    with pytest.raises(ValueError, match="The expiration timeframe in days cannot be zero or negative"):
        session_model.session_lifetime(-1)


def test_add_session_with_bad_type_index():
    with pytest.raises(IndexError, match="The type id should not be negative"):
        session_model.add_session(-1)


def test_add_session_with_unknown_type_index():
    with pytest.raises(IndexError, match="Type id is not existing in the database"):
        session_model.add_session(999)


def test_add_session_with_bad_days_input():
    with pytest.raises(ValueError, match="The number of days after which the session will expire cannot be negative"):
        session_model.add_session(1, -1)


def test_add_session():
    data = session_model.add_session(1, 1)
    print(data['session_uuid'])
    assert data['session_uuid'] is not None
    assert data['session_uuid'] is not ""
    assert data['creator_uuid'] is not None
    assert data['creator_uuid'] is not ""
    assert data['verifiers_uuid'] is not None
    assert data['verifiers_uuid'] is not ""
    assert data['type_id'] is not None
    assert data['type_id'] > 0


# noinspection PyTypeChecker
def test_update_session_with_wrong_type_type_id():
    with pytest.raises(TypeError, match="The argument should be an int"):
        session_model.update_session("", 1, 1)


# noinspection PyTypeChecker
def test_update_session_with_wrong_type_session_id():
    with pytest.raises(TypeError, match="The argument should be an int"):
        session_model.update_session(1, "", 1)


# noinspection PyTypeChecker
def test_update_session_with_wrong_type_s_lifetime():
    with pytest.raises(TypeError, match="The argument should be an int"):
        session_model.update_session(1, 1, "")


def test_update_session_with_session_id_negative():
    with pytest.raises(IndexError, match="The session id must be positive"):
        session_model.update_session(-1, 1, 1)


def test_update_session_with_type_id_negative():
    with pytest.raises(IndexError, match="The type id must be positive"):
        session_model.update_session(1, -1, 1)


def test_update_session_with_s_lifetime_negative():
    with pytest.raises(IndexError, match="The number of days after which the session will expire cannot be negative"):
        session_model.update_session(1, 1, -1)


def test_update_session_with_not_existing_session_id():
    with pytest.raises(IndexError, match="Session id is not existing in the database"):
        session_model.update_session(999, 1, 1)


def test_update_session_with_not_existing_type_id():
    with pytest.raises(IndexError, match="Type id is not existing in the database"):
        session_model.update_session(1, 999, 1)


def test_update_session(clean_up_db, setup_db_examples):
    session_model.update_session(1, 2, 4)
    data = session_model.get_session_by_id(1)
    assert data['type_id'] == 2


# noinspection PyTypeChecker
def test_get_session_by_id_wrong_type_session_id():
    with pytest.raises(TypeError, match="The session id should be an int"):
        session_model.get_session_by_id("")


def test_get_session_by_id_session_id_negative():
    with pytest.raises(IndexError, match="The session id must be positive"):
        session_model.get_session_by_id(-1)


def test_get_session_by_id_with_not_existing_session_id():
    with pytest.raises(IndexError, match="The session primary key don't exist in the database"):
        session_model.get_session_by_id(999)


def test_get_session_by_id(clean_up_db, setup_db_examples):
    data = session_model.get_session_by_id(1)
    assert data['id'] == 1
    assert data['uuid'] == "2"
    assert data['type_id'] == 1
    assert data['domain_id'] == 1
    assert data['verifier_token'] != "" and data['verifier_token'] is not None
    assert data['creator_token'] != "" and data['creator_token'] is not None


# noinspection PyTypeChecker
def test_get_session_by_uuid_wrong_type_session_uuid():
    with pytest.raises(TypeError, match="The argument should be an string"):
        session_model.get_session_by_uuid(1)


def test_get_session_by_uuid_session_uuid_empty():
    with pytest.raises(ValueError, match="The session uuid should not be empty"):
        session_model.get_session_by_uuid("")


def test_get_session_by_uuid_with_not_existing_session_uuid():
    with pytest.raises(IndexError, match="The session do not exist in the database"):
        session_model.get_session_by_uuid(" k k k j h j h k")


def test_get_session_by_uuid():
    data = session_model.get_session_by_uuid('2')
    assert data['id'] == 1
    assert data['uuid'] == "2"
    assert data['type_id'] == 1
    assert data['domain_id'] == 1
    assert data['verifier_token'] != "" and data['verifier_token'] is not None
    assert data['creator_token'] != "" and data['creator_token'] is not None


# noinspection PyTypeChecker
def test_get_type_id_from_type_wrong_type_type_value():
    with pytest.raises(TypeError, match="Type value should be a string"):
        session_model.get_type_id_from_type(1)


def test_get_type_id_from_type_type_value_empty():
    with pytest.raises(ValueError, match="Type cannot be empty"):
        session_model.get_type_id_from_type("")


def test_get_type_id_from_type_with_not_existing_type_value():
    with pytest.raises(IndexError, match="Type value do not exist in the database"):
        session_model.get_type_id_from_type(" k k k j h j h k")


def get_type_id_from_type(clean_up_db, setup_db_examples):
    data = session_model.get_type_id_from_type("all_words_together")
    assert data['id'] == 1
    assert data['type'] == "all_words_together"


# noinspection PyTypeChecker
def test_type_id_exists_wrong_type():
    with pytest.raises(TypeError, match="Type id should be a integer"):
        session_model.type_id_exists("")


def test_type_id_exists_negative_value():
    with pytest.raises(IndexError, match="Type id cannot be negative"):
        session_model.type_id_exists(-1)


def test_type_id_exists():
    assert session_model.type_id_exists(1)
    assert not session_model.type_id_exists(99)


# noinspection PyTypeChecker
def test_session_id_exists_wrong_type():
    with pytest.raises(TypeError, match="Session identifier should be an integer"):
        session_model.session_id_exists("")


def test_session_id_exists_negative_value():
    with pytest.raises(IndexError, match="Session id cannot be negative"):
        session_model.session_id_exists(-1)


def test_session_id_exists():
    assert session_model.session_id_exists(1)
    assert not session_model.session_id_exists(999)


# noinspection PyTypeChecker
def test_session_uuid_exists_wrong_type():
    with pytest.raises(TypeError, match="Session unique identifier should be a string"):
        session_model.session_uuid_exists(1)


def test_session_uuid_exists_empty():
    with pytest.raises(ValueError, match="Session unique identifier cannot be empty"):
        session_model.session_uuid_exists("")


# noinspection PyTypeChecker
def test_get_session_id_from_uuid_wrong_type():
    with pytest.raises(TypeError, match="Session unique identifier should be a string"):
        session_model.get_session_id_from_uuid(1)


def test_get_session_id_from_uuid_empty():
    with pytest.raises(ValueError, match="Session unique identifier cannot be empty"):
        session_model.get_session_id_from_uuid("")


def test_get_session_id_from_uuid_with_not_existing_value():
    with pytest.raises(IndexError, match="Session uuid do not exist in the database"):
        session_model.get_session_id_from_uuid(" k k k j h j h k")


def test_get_session_id_from_uuid():
    assert 1 == session_model.get_session_id_from_uuid("2")


def test_get_all_types(clean_up_db, setup_db_examples):
    data = session_model.get_all_types()
    assert len(data) == 3
    assert data[0]['type'] == "all_words_together"

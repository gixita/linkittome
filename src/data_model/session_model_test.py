import pytest
from src.data_model import session_model


def test_create_session_with_bad_type_index():
    with pytest.raises(IndexError, match="The type id should not be negative"):
        session_model.create_session(-1)


def test_create_session_with_unknown_type_index():
    with pytest.raises(IndexError, match="Type id is not existing in the database"):
        session_model.create_session(999)


def test_create_session_with_bad_days_input():
    with pytest.raises(ValueError, match="The number of days after which the session will expire cannot be negative"):
        session_model.create_session(1, -1)


def test_create_session():
    data = session_model.create_session(1, 1)
    print(data['session_uuid'])
    assert data['session_uuid'] is not None
    assert data['session_uuid'] is not ""
    assert data['creator_uuid'] is not None
    assert data['creator_uuid'] is not ""
    assert data['verifiers_uuid'] is not None
    assert data['verifiers_uuid'] is not ""
    assert data['type_id'] is not None
    assert data['type_id'] > 0





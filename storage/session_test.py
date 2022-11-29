import session
import pytest
import db


def test_add_session(clean_up_db):
    session.add_session('51651', '561615561', '651315', 1)
    session_data = session.get_session('51651')
    print(session_data)
    assert '561615561' == session_data['creator_token']


def test_update_session(clean_up_db):
    session.add_session('51651', '561615561', '651315', 1)
    session.update_session(1, 2)
    session_data = session.get_session('51651')
    assert 2 == session_data['type_id']





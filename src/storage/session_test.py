from src.storage import session


def test_add_session(clean_up_db):
    session.add_session('51651', '561615561', '651315', 1, 3)
    session_data = session.get_session('51651')
    assert '561615561' == session_data['creator_token']


def test_update_session(clean_up_db):
    session.add_session('51651', '561615561', '651315', 1, 3)
    session.update_session(1, 2, 3)
    session_data = session.get_session('51651')
    assert 2 == session_data['type_id']

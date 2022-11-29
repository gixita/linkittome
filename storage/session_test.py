import session


def test_add_session():
    session.add_session('51651', '561615561', '651315', 1)
    session_data = session.get_session('51651')
    assert '561615561' == session_data['creator_token']
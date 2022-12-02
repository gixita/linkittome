from src.storage import session


def test_add_session(clean_up_db):
    session.add_session('51651', '561615561', '651315', 1, 3)
    session_data = session.get_session_by_uuid('51651')
    assert '561615561' == session_data['creator_token']


def test_update_session(clean_up_db):
    session.add_session('51651', '561615561', '651315', 1, 3)
    session.update_session(1, 2, 3)
    session_data = session.get_session_by_uuid('51651')
    assert 2 == session_data['type_id']


def test_session_lifetime_with_valid_data():
    if not session.session_lifetime(5) == "+5 days":
        raise ValueError("The string output of the session lifetime do not match the requirements")

# TODO get_session_by_id


def test_get_type_id_from_type():
    if not session.get_type_id_from_type("all_words_together")['id'] == 1:
        raise Exception("The value in")


def test_type_id_exists(clean_up_db, setup_db_examples):
    if not session.type_id_exists(1):
        raise IndexError("The id 1 should exist in the database")
    if session.type_id_exists(999):
        raise IndexError("The id 999 should NOT exist in the database")


def test_session_id_exists():
    assert session.session_id_exists(1)
    assert not session.session_id_exists(999)


def test_session_uuid_exists():
    if not session.session_uuid_exists("2"):
        raise IndexError("The uuid '2' should exist in the database")
    if session.session_uuid_exists("s k l d j f l k j d"):
        raise IndexError("Random uuid should NOT exist in the database")

# TODO def test_session_uuid_exists(session_uuid: str) -> bool:


def test_get_all_types():
    data = session.get_all_types()
    if len(data) != 3:
        raise Exception("The correct types are not retrieved")
    if data[0]['id'] != 1:
        raise ValueError("The order of the data is not correct")
    if data[0]['type'] != "all_words_together":
        raise ValueError("The type value is not retrieve correctly")

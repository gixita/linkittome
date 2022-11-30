import uuid
from ..storage import session


def session_lifetime(days=3) -> int:
    return days

def type_id_exists(type_id: int) -> bool:
    pass


def create_session(type_id: int):
    session_uuid = str(uuid.uuid4())
    creator_uuid = str(uuid.uuid4())
    verifiers_uuid = str(uuid.uuid4())
    session.add_session(session_uuid, creator_uuid, verifiers_uuid, 1, session_lifetime())
    session.get_type_id_from_type("type")
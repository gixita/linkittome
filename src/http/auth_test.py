import pytest
from src.http import auth
from datetime import datetime, timedelta
import jwt


def test_generate_token_is_string():
    data = auth.generate_token(False)
    assert isinstance(data, str)
    assert data is not None and data is not ""
    assert auth.generate_token(False) != auth.generate_token(False)


def generate_bad_token(secret: str) -> str:
    return jwt.encode({
        'user_uuid_wrong_field': "Yes it is a token",
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, secret)


def test_get_user_uuid_from_token():
    bad_secret = {"Authorization": "Bearer " + generate_bad_token("test")}
    with pytest.raises(ValueError, match="Bearer token is invalid"):
        auth.get_user_uuid_from_token(bad_secret, False)
    bad_field = {"Authorization": "Bearer " + generate_bad_token("SuperSecretForTests")}
    with pytest.raises(ValueError, match="Token valid but do not fulfill server requirements"):
        auth.get_user_uuid_from_token(bad_field, False)


def test_headers_contains_authorization():
    good_data = {"Authorization": "Bearer ENCODED_TOKEN"}
    bad_data = {"SomethingElse": "Random value"}
    assert auth.headers_contains_authorization(good_data)
    assert not auth.headers_contains_authorization(bad_data)


def test_get_token_from_headers():
    good_data = {"Authorization": "Bearer ENCODED_TOKEN"}
    bad_data = {"SomethingElse": "Random value"}
    assert "ENCODED_TOKEN" == auth.get_token_from_headers(good_data)
    with pytest.raises(ValueError, match="Authorization section missing from headers"):
        auth.get_token_from_headers(bad_data)

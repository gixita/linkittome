import uuid
import jwt
from datetime import datetime, timedelta
from flask import current_app


def get_config_secret(is_prod) -> str:
    if is_prod:
        return current_app.config['SECRET_KEY']
    else:
        return "SuperSecretForTests"


def generate_token(is_prod=True) -> str:
    return jwt.encode({
        'user_uuid': str(uuid.uuid4()),
        'exp': datetime.utcnow() + timedelta(minutes=30)
        }, get_config_secret(is_prod))


def get_user_uuid_from_token(headers: dict[str, str], is_prod=True) -> str:
    try:
        secret = current_app.config['SECRET_KEY'] if is_prod else "SuperSecretForTests"
        data = jwt.decode(get_token_from_headers(headers), secret, algorithms=["HS256"])
    except Exception:
        raise ValueError("Bearer token is invalid")
    if 'user_uuid' not in data.keys():
        raise ValueError("Token valid but do not fulfill server requirements")
    return data['user_uuid']


def headers_contains_authorization(headers: dict[str, str]) -> bool:
    return True if 'Authorization' in headers else False


def get_token_from_headers(headers: dict[str, str]) -> str:
    if not headers_contains_authorization(headers):
        raise ValueError("Authorization section missing from headers")
    return headers['Authorization'][7:]

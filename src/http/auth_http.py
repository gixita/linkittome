from functools import wraps
from flask import Blueprint, jsonify, request, make_response
from src.http import auth as auth
auth_http = Blueprint('auth_http', __name__, url_prefix='/v1')


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            user_uuid = auth.get_user_uuid_from_token(request.headers)
        except Exception as e:
            return {'error': str(e)}, 401
        return f(user_uuid, *args, **kwargs)
    return decorator


@auth_http.route("/unprotected", methods=['GET'])
def unprotected():
    return "hello", 200


@auth_http.route("/login", methods=['GET'])
def login():
    return make_response(jsonify({'token': auth.generate_token()}), 201)


@auth_http.route("/protected", methods=['GET'])
@token_required
def protected(user_uuid):
    print(user_uuid)
    return "hello", 200

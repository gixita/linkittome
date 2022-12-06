import json

from flask import Blueprint, jsonify, request
from src.data_model import session_model
from src.http import check_quality_http as quality

session_http = Blueprint('session_http', __name__, url_prefix='/v1')


@session_http.route("/create_session/<int:type_id>", methods=['POST'])
def create_session(type_id: str):
    """
    Create a new session with a specific type.
    Body payload should be empty.
    :param type_id: integer private key of the table session type
    :raise HTTPCODE_401: if type_id is not correct
    :return: HTTPCODE_201 session created successfully
    """
    try:
        response = session_model.add_session(int(type_id))
    except Exception as e:
        return jsonify({'error': str(e)}), 401
    return jsonify(response), 201


@session_http.route("/session/<string:session_uuid>/<string:creator_uuid>", methods=['GET'])
@session_http.route("/session/<string:session_uuid>", defaults={'creator_uuid': None}, methods=['GET'])
def get_session(session_uuid: str, creator_uuid: str):
    """
    :raise HTTPCODE_401: if creator or session uuid are invalid
    :return: HTTPCODE_200 success
    """
    try:
        if creator_uuid is None:
            return jsonify(session_model.get_session_by_uuid(session_uuid)), 200
        else:
            return jsonify(session_model.get_session_by_creator_uuid(session_uuid, creator_uuid)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401


@session_http.route("/update_session/<string:session_uuid>/<string:creator_uuid>", methods=['PUT'])
@session_http.route("/update_session/<string:session_uuid>", defaults={'creator_uuid': None}, methods=['PUT'])
def update_session(session_uuid: str, creator_uuid: str):
    """
    :raise HTTPCODE_400: if content-type is not application/json
    :raise HTTPCODE_401: session uuid or type_id are invalid
    :raise HTTPCODE_403: creator uuid is not valid
    :return: HTTPCODE_200 success
    """
    if creator_uuid is None:
        return jsonify({'error': "Creator uuid missing"}), 403
    try:
        quality.check_content_type_headers(request.headers)
        json_payload = request.json
        quality.check_type_id(json_payload)
        session_id = session_model.get_session_id_from_uuid(session_uuid)
        session_model.update_session(session_id, json_payload['type_id'])
        return jsonify(session_model.get_session_by_creator_uuid(session_uuid, creator_uuid)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401


@session_http.route("/get_types", methods=['GET'])
def get_all_types():
    """
    Return all types from the app
    Example:
     .. code-block:: json
    [
        {
            "id": 1, "type": "all_words_together"
        }
    ]

    :return: list of dict in json format with id and type
    """
    return json.dumps([dict(i) for i in session_model.get_all_types()]), 200

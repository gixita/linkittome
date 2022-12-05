import json
from flask import Blueprint, jsonify, request
from src.data_model import session_model, word_model
from src.http import check_quality_http as quality

word_http = Blueprint('word_http', __name__, url_prefix='/v1')


@word_http.route("/word/<string:session_uuid>/<string:creator_uuid>", methods=['POST'])
def add_word(session_uuid: str, creator_uuid):
    """
    Add a new word to the session

    :raise HTTPCODE_400: if content-type is not application/json
    :raise HTTPCODE_401: if creator or session uuid are invalid
    :return: HTTPCODE_200 success
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json_payload = request.json
    else:
        return jsonify({'error': 'Content-Type not supported'}), 400
    try:
        # Check if creator_uuid is valid and retrieve session id
        session_data = session_model.get_session_by_creator_uuid(session_uuid, creator_uuid)
        quality.check_word_value(json_payload)
        quality.check_ordering(json_payload)
        word_model.add_word(json_payload['word_value'], session_data['id'], json_payload['ordering'])
        return jsonify({}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 401


@word_http.route("/word/<string:session_uuid>/<string:creator_uuid>", methods=['PUT'])
def update_word(session_uuid: str, creator_uuid):
    """
    Update a word of the session base on its primary key

    The body should contain the following keys :

    - 'id' : integer key of the word to modify
    - 'word_value' : string containing the updated value for the word
    - 'ordering' : integer new integer value for the order of the word in the session

    :raise HTTPCODE_400: if content-type is not application/json
    :raise HTTPCODE_401: if creator or session uuid are invalid
    :return: HTTPCODE_200 success
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json_payload = request.json
    else:
        return jsonify({'error': 'Content-Type not supported'}), 400
    try:
        # Check if creator_uuid is valid and retrieve session id
        session_data = session_model.get_session_by_creator_uuid(session_uuid, creator_uuid)
        quality.check_word_id(json_payload)
        quality.check_word_value(json_payload)
        quality.check_ordering(json_payload)
        word_model.update_word(json_payload['word_id'],
                               json_payload['word_value'],
                               json_payload['ordering'],
                               session_data['session_id'])
        word = word_model.get_word_by_id(json_payload['word_id'])
        return jsonify({"word_id": word['word_id'],
                        "word_value": word['word'],
                        "ordering": word['ordering']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401


@word_http.route("/word/<string:session_uuid>/<string:creator_uuid>", methods=['DELETE'])
def delete_word(session_uuid: str, creator_uuid):
    """
    Update a word of the session base on its primary key

    The body should contain the following keys :

    - 'id' : integer key of the word to modify
    - 'word_value' : string containing the updated value for the word
    - 'ordering' : integer new integer value for the order of the word in the session

    :raise HTTPCODE_400: if content-type is not application/json
    :raise HTTPCODE_401: if creator or session uuid are invalid
    :return: HTTPCODE_200 success
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json_payload = request.json
    else:
        return jsonify({'error': 'Content-Type not supported'}), 400
    try:
        # Check if creator_uuid is valid and retrieve session id
        session_data = session_model.get_session_by_creator_uuid(session_uuid, creator_uuid)
        quality.check_word_id(json_payload)
        word_model.delete_word(json_payload['word_id'], session_data['id'])
        return jsonify({}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401


@word_http.route("/words/<string:session_uuid>", methods=['GET'])
def get_all_words(session_uuid: str):
    """
    Get all words linked to the session

    :param session_uuid: session uuid
    :raise HTTPCODE_401: if type_id is not correct
    :return: HTTPCODE_200 successfully retrieved words for the session
    """
    try:
        response = word_model.get_all_words(session_model.get_session_id_from_uuid(session_uuid))
    except Exception as e:
        return jsonify({'error': str(e)}), 401
    return json.dumps([dict(i) for i in response]), 200

from flask import Flask, send_from_directory, request
from flask_swagger_ui import get_swaggerui_blueprint
import sqlite3
import uuid

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/g4m/api/v1/get_words/<session_uuid>", methods=['get'])
def get_words(session_uuid):
    words = ""
    print(session_uuid)
    try:
        pass

    except:
        msg = "error in search words operation"
        return {msg}, 400

    finally:
        return {}, 200


@app.route("/g4m/api/v1/word/<session_uuid>/<creator_uuid>", methods=['POST', 'PUT'])
def word(session_uuid, creator_uuid):
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
    else:
        return {'Content-Type not supported!'}, 400
    if json['word'] is None:
        return {'Missing data word'}, 400
    if json['ordering'] is None:
        json['ordering'] = 0
    try:
        pass
    except:
        msg = "error in insert operation"
        return {msg}, 400

    finally:
        return {}, 201


@app.route("/g4m/api/v1/create_session", methods=['POST'])
def create_session():
    session_uuid = str(uuid.uuid4())
    creator_uuid = str(uuid.uuid4())
    verifiers_uuid = str(uuid.uuid4())
    content_type = request.headers.get('Content-Type')
    type_id = 0
    if content_type == 'application/json':
        json = request.json
    else:
        return {'Content-Type not supported!'}, 400
    if json['type'] == "all_words_together":
        type_id = 1
    try:
        pass
    except:
        msg = "error in insert operation"
        return {msg}, 400

    finally:
        return {"session_uuid": session_uuid,
                "creator_uuid": creator_uuid,
                "verifiers_uuid": verifiers_uuid}, 201




@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory('src/static', path)


SWAGGER_URL = "/api/v1/docs"
API_URL = "/static/settings-swagger-v1.json"


swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Link it to me"
    },
)

app.register_blueprint(swagger_ui_blueprint)


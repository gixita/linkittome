from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/g4m/api/v1/get_words/<session_uuid>", methods=['get'])
def get_words(session_uuid):
    try:
        pass
    except:
        msg = "error"
        return {msg}, 400
    finally:
        return {}, 200


@app.route("/g4m/api/v1/word/<session_uuid>/<creator_uuid>", methods=['POST', 'PUT'])
def word(session_uuid, creator_uuid):
    pass


@app.route("/g4m/api/v1/create_session", methods=['POST'])
def create_session():
    pass


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


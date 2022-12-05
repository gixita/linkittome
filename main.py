from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from src.http import session_http, auth_http

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.register_blueprint(session_http.session_http)
app.register_blueprint(auth_http.auth_http)


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


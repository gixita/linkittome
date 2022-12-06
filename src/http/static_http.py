from flask import Blueprint, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
static_http = Blueprint('static_http', __name__, url_prefix='')


@static_http.route("/static/<path:path>")
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
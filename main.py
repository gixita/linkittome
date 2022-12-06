import os
from flask import Flask, send_from_directory

from src.http import session_http, auth_http, word_http, static_http
from src.frontend import home


template_dir = os.path.abspath('./src/frontend/templates')
static_dir = os.path.abspath('./src/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.config['SECRET_KEY'] = 'your secret key'
app.register_blueprint(session_http.session_http)
app.register_blueprint(auth_http.auth_http)
app.register_blueprint(word_http.word_http)
app.register_blueprint(home.home_frontend)
app.register_blueprint(static_http.swagger_ui_blueprint)
app.register_blueprint(static_http.static_http)




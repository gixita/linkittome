from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import sqlite3
import uuid

app = Flask(__name__)
db = "links.db"

def exec_db(command):
    conn = sqlite3.connect('links.db')
    conn.execute(command)
    conn.close()


def get_type_id(type):
    conn = sqlite3.connect('links.db')
    conn.execute("SELECT id from type where type='"+type+"'")
    conn.close()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/g4m/api/v1/get_words/<session_uuid>", methods=['get'])
def get_words(session_uuid):
    words = ""
    print(session_uuid)
    try:
        with sqlite3.connect(db) as con:
            con.row_factory = sqlite3.Row
            words = con.execute('SELECT word.word as word, word.ordering as ordering, session.uuid as session_uuid '
                                'FROM word LEFT JOIN session ON word.session_id = session.id '
                                'WHERE session.uuid = ? ORDER BY word.ordering;', (session_uuid,)).fetchall()
            # words = con.execute('SELECT * FROM word').fetchall()
            for word in words:
                print(word['word'])
                print(word['session_uuid'])

    except:
        msg = "error in search words operation"
        return {msg}, 400

    finally:
        return {}, 200
        con.close()


@app.route("/g4m/api/v1/create_session", methods=['POST'])
def create_session():
    session_uuid = str(uuid.uuid4())
    creator_uuid = str(uuid.uuid4())
    verifiers_uuid = str(uuid.uuid4())
    try:
        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO session (uuid,type_id,domain_id,verifier_token, creator_token, expiration_date) "
                        "VALUES (?,?,?,?,?,date('now', '+3 days'))",
                        (session_uuid, 1, 1, verifiers_uuid, creator_uuid))
            con.commit()
            msg = "New session successfully stored"
    except:
        con.rollback()
        msg = "error in insert operation"
        return {msg}, 400

    finally:
        return {"session_uuid": session_uuid,
                "creator_uuid": creator_uuid,
                "verifiers_uuid": verifiers_uuid}, 201
        con.close()



@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory('static', path)


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


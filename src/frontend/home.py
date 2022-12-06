from flask import Blueprint, render_template

home_frontend = Blueprint('home_frontend', __name__, url_prefix='')


@home_frontend.route("/", methods=['GET'])
def home():
    return render_template('index.html')


@home_frontend.route("/create", methods=['GET'])
def create():
    return render_template('create.html')


@home_frontend.route("/questions", methods=['GET'])
def questions():
    return render_template('questions.html')

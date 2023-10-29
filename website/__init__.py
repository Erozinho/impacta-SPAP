from flask import Flask
from website.page import page
import os

user = os.path.expanduser('~')
dir_root = user + '\\Downloads'

def create_app():
    app = Flask(__name__)
    app.secret_key = "BANCO123"
    app.config['UPLOAD_FOLDER'] = dir_root
    app.config['MAX_CONTENT_LENGTH'] = 10000000
    # app.config["SESSION_COOKIE_SAMESITE"] = "None"


    app.register_blueprint(page, url_prefix="/")

    return app

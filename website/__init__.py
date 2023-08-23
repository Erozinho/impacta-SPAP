from flask import Flask
from website.page import page

def create_app():
    app = Flask(__name__)
    app.secret_key = "BANCO123"

    app.register_blueprint(page, url_prefix="/")

    return app

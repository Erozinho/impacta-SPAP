from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config ['SECRET KEY'] = 'BANCO123'

    from website.page import page

    app.register_blueprint(page, url_prefix="/")


    return app

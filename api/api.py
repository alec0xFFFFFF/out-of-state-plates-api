from flask import Flask

def create_api():
    app = Flask(__name__)

    # Configuration and other setup here

    from api.routes import init_app
    init_app(app)

    return app


from flask import Flask
from app.routes import gateway_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(gateway_bp)

    return app

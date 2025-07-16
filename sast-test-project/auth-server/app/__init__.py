from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from config import Config

db = SQLAlchemy()
oauth = OAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    oauth.init_app(app)
    
    from .oauth2 import oauth2_bp
    app.register_blueprint(oauth2_bp)
    
    return app

app = create_app()
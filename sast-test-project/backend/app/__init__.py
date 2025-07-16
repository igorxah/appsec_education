from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # УЯЗВИМОСТЬ: Небезопасные CORS настройки
    CORS(app, resources={r"/*": {"origins": app.config['CORS_ORIGINS']}})
    
    db.init_app(app)
    
    from .auth import auth_bp
    from .crud import crud_bp
    from .discord import discord_bp
    from .telegram import telegram_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(crud_bp)
    app.register_blueprint(discord_bp)
    app.register_blueprint(telegram_bp)
    
    return app

app = create_app()
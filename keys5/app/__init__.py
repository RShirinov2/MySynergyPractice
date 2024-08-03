from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import routes
        routes.init_routes(app)  # Добавьте эту строку
        db.create_all()

    return app

from app import models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

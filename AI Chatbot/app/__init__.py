from flask import Flask
from app.config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager

# import sqlalchemy as sa
# import sqlalchemy.orm as so
# from app.models import User, Chat

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

# @app.shell_context_processor
# def make_shell_context():
#     return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Chat': Chat}

from app import routes, models

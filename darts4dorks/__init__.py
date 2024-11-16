from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app, add_models_to_shell=True)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"


from darts4dorks import routes, models

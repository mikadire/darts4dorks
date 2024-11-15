from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app, add_models_to_shell=True)
migrate = Migrate(app, db)


from darts4dorks import routes, models
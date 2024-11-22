from flask import Blueprint

bp = Blueprint("main", __name__)

from darts4dorks.main import routes
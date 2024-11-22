from flask import Blueprint

bp = Blueprint("user", __name__, url_prefix="/user")

from darts4dorks.auth import routes
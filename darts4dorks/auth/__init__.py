from flask import Blueprint

bp = Blueprint("auth", __name__, url_prefix="/auth")

from darts4dorks.auth import routes

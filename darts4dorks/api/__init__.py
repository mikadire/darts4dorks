from flask import Blueprint

bp = Blueprint("api", __name__, url_prefix="/api")

from darts4dorks.api import stats, tokens

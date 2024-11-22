from flask import Blueprint

bp = Blueprint("errors", __name__)

from darts4dorks.errors import handlers


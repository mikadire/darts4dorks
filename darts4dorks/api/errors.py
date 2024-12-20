from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from darts4dorks.api import bp


def error_response(status_code, message=None):
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    if message:
        payload["message"] = message
    return payload, status_code


@bp.errorhandler(HTTPException)
def handle_exception(e):
    return error_response(e.code)

from flask import render_template, request
from darts4dorks import db
from darts4dorks.errors import bp
from darts4dorks.api.errors import error_response as api_error_response


def wants_json_response():
    return (
        request.accept_mimetypes["application/json"]
        >= request.accept_mimetypes["text/html"]
    )

@bp.app_errorhandler(403)
def forbidden_error(error):
    if wants_json_response():
        return api_error_response(403)
    return render_template("errors/403.html"), 403


@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template("errors/500.html"), 500

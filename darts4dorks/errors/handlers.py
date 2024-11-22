from flask import render_template
from darts4dorks import db
from darts4dorks.errors import bp

# Custom error handlers
@bp.errorhandler(404)
def error_404(error):
    return render_template("errors/404.html"), 404

@bp.errorhandler(403)
def error_403(error):
    return render_template("errors/403.html"), 403

@bp.errorhandler(500)
def error_500(error):
    db.session.rollback()
    return render_template("errors/500.html"), 500

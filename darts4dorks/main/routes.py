from flask import render_template, flash, request, jsonify
from flask_login import current_user, login_required
from darts4dorks import db
from darts4dorks.main import bp
from darts4dorks.models import Attempt


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("index.html")


@bp.route("/round_the_clock", methods=["GET"])
@login_required
def round_the_clock():
    result = current_user.get_active_session_and_target()
    if result is None:
        session = current_user.create_session()
        target = 1
    else:
        session, target = result
        target += 1
        flash("You had an existing game going.")
        if not target:
            target = 1
    return render_template(
        "round_the_clock.html",
        title="Round the Clock",
        session_id=session.id,
        target=target,
    )


@bp.route("/attempt", methods=["POST"])
@login_required
def attempt():
    data = request.get_json()
    attempt = Attempt(
        target=data["target"],
        darts_thrown=data["darts_thrown"],
        session_id=data["session_id"],
    )
    db.session.add(attempt)
    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Attempt successfully saved."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

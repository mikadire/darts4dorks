from flask import render_template, flash, request, url_for
from flask_login import current_user, login_required
from darts4dorks import db
from darts4dorks.main import bp
from darts4dorks.models import Session, Attempt


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("index.html")


@bp.route("/round_the_clock")
@login_required
def round_the_clock():
    result = current_user.get_active_session_and_target()
    if result is None:
        session = current_user.create_session()
        db.session.commit()
        target = 1
    else:
        flash("You had an existing game going.")
        session, target = result
        if target is None:
            target = 1
        else:
            target += 1
    return render_template(
        "round_the_clock.html",
        title="Round the Clock",
        session_id=session.id,
        target=target,
    )


@bp.route("/submit_attempt", methods=["POST"])
@login_required
def submit_attempt():
    data = request.get_json()
    attempt = Attempt(
        target=data["target"],
        darts_thrown=data["darts_thrown"],
        session_id=data["session_id"],
    )
    db.session.add(attempt)

    try:
        db.session.commit()
        return {"success": True, "message": "Attempt successfully saved."}, 201
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}, 500


@bp.route("/undo_attempt", methods=["POST"])
@login_required
def undo_attempt():
    data = request.get_json()
    attempt = db.session.scalar(
        db.select(Attempt).where(
            Attempt.session_id == data["session_id"], Attempt.target == data["target"]
        )
    )
    db.session.delete(attempt)

    try:
        db.session.commit()
        return {"success": True, "message": "Attempt successfully saved."}, 200
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}, 500


@bp.route("/redirect_game_over", methods=["POST"])
@login_required
def redirect_game_over():
    data = request.get_json()
    session = db.session.get(Session, data["session_id"])
    session.ended = True

    try:
        db.session.commit()
        url = url_for("main.game_over")
        return {"success": True, "url": url}, 200
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}, 500


@bp.route("/game_over")
def game_over():
    return render_template("game_over.html")

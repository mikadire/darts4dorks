from flask import render_template, flash, request, url_for, redirect, abort
from flask_login import current_user, login_required
from darts4dorks import db
from darts4dorks.main import bp
from darts4dorks.models import User, Session, Attempt
from darts4dorks.stats import get_rtc_stats
from darts4dorks.auth.forms import RegistrationForm


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created.", "success")
        return redirect(url_for("auth.login"))
    return render_template("index.html", form=form)


@bp.route("/round_the_clock")
@login_required
def round_the_clock():
    user_id = current_user.id
    result = current_user.get_active_session_and_target()
    if result is None:
        session = current_user.create_session()
        db.session.commit()
        target = 1
    else:
        flash("You had an existing game going.", "info")
        session, target = result
        if target is None:
            target = 1
        else:
            target += 1
    return render_template(
        "round_the_clock.html",
        title="Round the Clock",
        user_id=user_id,
        session_id=session.id,
        target=target,
    )


@bp.route("/submit_attempt", methods=["POST"])
@login_required
def submit_attempt():
    data = request.get_json()
    session_id = data["session_id"]
    target = data["target"]
    darts_thrown = data["darts_thrown"]

    try:
        session_id = int(data["session_id"])
        target = int(data["target"])
        darts_thrown = int(data["darts_thrown"])
    except (ValueError, TypeError):
        return {"success": False, "message": "Invalid data types."}, 400

    session = db.session.get(Session, session_id)
    if not session or current_user.id != session.user_id:
        return {"success": False, "message": "Unauthorized session access"}, 403

    if darts_thrown < 1 or target < 1:
        return {"success": False, "message": "Invalid values"}, 400

    attempt = Attempt(
        target=target,
        darts_thrown=darts_thrown,
        session_id=session_id,
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
    session_id = data["session_id"]
    target = data["target"]

    try:
        session_id = int(data["session_id"])
        target = int(data["target"])
    except (ValueError, TypeError):
        return {"success": False, "message": "Invalid data types."}, 400

    session = db.session.get(Session, session_id)
    if not session or current_user.id != session.user_id:
        return {"success": False, "message": "Unauthorized session access"}, 403

    attempt = db.session.scalar(
        db.select(Attempt).where(
            Attempt.session_id == session_id, Attempt.target == target
        )
    )

    if not attempt:
        return {"success": False, "message": "Attempt not found."}, 404

    db.session.delete(attempt)

    try:
        db.session.commit()
        return {"success": True, "message": "Attempt successfully deleted."}, 200
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}, 500


@bp.route("/redirect_game_over", methods=["POST"])
@login_required
def redirect_game_over():
    data = request.get_json()
    session_id = data["session_id"]

    try:
        session_id = int(data["session_id"])
    except (KeyError, ValueError, TypeError):
        return {"success": False, "message": "Invalid or missing session ID"}, 400

    session = db.session.get(Session, session_id)
    if not session or current_user.id != session.user_id:
        return {"success": False, "message": "Unauthorized session access"}, 403

    session.ended = True

    try:
        db.session.commit()
        url = url_for("main.game_over", session_id=session_id)
        return {"success": True, "url": url}, 200
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}, 500


@bp.route("/game_over/<int:session_id>")
@login_required
def game_over(session_id):
    session = db.session.get(Session, session_id)

    if current_user.id != session.user_id:
        abort(403)

    if not session or not session.ended:
        abort(404)

    return render_template(
        "game_over.html",
        title="Game Over",
        user_id=current_user.id,
        session_id=session_id,
    )


@bp.route("/rtc_stats")
@login_required
def rtc_stats():
    user_id = current_user.id
    return get_rtc_stats(user_id)

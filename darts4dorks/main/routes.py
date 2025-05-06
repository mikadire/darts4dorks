from flask import render_template, flash, request, url_for, redirect, abort, current_app
from flask_login import current_user, login_required, login_user
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from darts4dorks import db
from darts4dorks.main import bp
from darts4dorks.models import User, Session, Attempt
from darts4dorks.utils import validate_rtc_data
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
        flash("Your account has been created. You are now logged in.", "success")
        login_user(user)
        return redirect(url_for("auth.login"))
    return render_template("index.html", form=form)


@bp.route("/round_the_clock")
@login_required
def round_the_clock():
    return render_template(
        "round_the_clock.html",
        title="Round the Clock",
    )


@bp.route("/submit_game", methods=["POST"])
@login_required
def submit_game():
    try:
        data = validate_rtc_data(request.get_json())
    except ValidationError as e:
        return {"success": False, "errors": e.errors()}, 400

    session = current_user.create_session()
    session_id = session.id
    session.ended = True

    attempts = [
        Attempt(
            target=attempt.target,
            darts_thrown=attempt.darts_thrown,
            session_id=session_id,
        )
        for attempt in data
    ]
    db.session.add_all(attempts)

    try:
        db.session.commit()
        url = url_for("main.game_over", session_id=session_id)
        return {"success": True, "url": url, "message": "Game successfully saved."}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.exception("Database commit failed")
        return {"success": False, "message": "An internal error has occurred."}, 500


@bp.route("/game_over/<int:session_id>")
@login_required
def game_over(session_id):
    session = db.session.get(Session, session_id)

    if not session or not session.ended or current_user.id != session.user_id:
        abort(404)

    stats = get_rtc_stats(current_user.id)

    return render_template(
        "game_over.html",
        title="Game Over",
        data=stats,
        session_id=session_id,
    )

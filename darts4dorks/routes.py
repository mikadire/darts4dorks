from flask import render_template, url_for, redirect, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import select
from urllib.parse import urlsplit
from darts4dorks import app, db
from darts4dorks.forms import (
    LoginForm,
    RegistrationForm,
    UpdateAccountForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
)
from darts4dorks.models import User, Attempt
from darts4dorks.email import send_password_reset_email


@app.route("/test_error")
def test_error():
    app.logger.error("This is a test error for email logging!")
    return "Error logged."


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(select(User).where(User.email == form.email.data))
        if user is None or not user.verify_password(form.password.data):
            flash("Invalid username or password.", "danger")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")


@app.route("/update_account", methods=["GET", "POST"])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated.", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("update_account.html", title="Update Account", form=form)


@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password.")
        return redirect(url_for("login"))
    return render_template(
        "reset_password_request.html", title="Reset Password", form=form
    )


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user = User.verify_passowrd_reset_token(token)
    if not user:
        flash("That is an invalid or expired token.", "warning")
        return redirect(url_for("index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.")
        return redirect(url_for("login"))
    return render_template("reset_password.html", form=form)


@app.route("/round_the_clock", methods=["GET"])
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


@app.route("/attempt", methods=["POST"])
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

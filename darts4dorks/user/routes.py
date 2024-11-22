from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from darts4dorks import db
from darts4dorks.user import bp
from darts4dorks.user.forms import UpdateAccountForm


@bp.route("/account")
@login_required
def account():
    return render_template("user/account.html", title="Account")


@bp.route("/update_account", methods=["GET", "POST"])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated.", "success")
        return redirect(url_for("user.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template(
        "user/update_account.html", title="Update Account", form=form
    )

from flask import render_template, current_app
from darts4dorks.email import send_email


def send_password_reset_email(user):
    token = user.get_password_reset_token()
    send_email(
        "[Darts for Dorks] Reset Your Password",
        sender=current_app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token),
    )

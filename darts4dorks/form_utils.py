from flask import flash
from flask_login import current_user, login_user
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, Length, ValidationError

from darts4dorks import db
from darts4dorks.models import User


def validate_username(self, username):
    if current_user.is_active and username.data == current_user.username:
        return
    else:
        user = db.session.scalar(db.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )


def validate_email(self, email):
    if current_user.is_active and email.data == current_user.email:
        return
    else:
        user = db.session.scalar(db.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError("Please use a different email address.")


class UniqueUserFieldMixin:
    username = StringField(
        "Username", validators=[DataRequired(), Length(max=32), validate_username]
    )


class UniqueEmailFieldMixin:
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(max=128), validate_email]
    )


class PasswordFieldMixin:
    password = PasswordField("Password", validators=[DataRequired(), Length(max=256)])

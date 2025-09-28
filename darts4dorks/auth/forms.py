from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo

from darts4dorks.form_utils import (
    PasswordFieldMixin,
    UniqueEmailFieldMixin,
    UniqueUserFieldMixin,
)


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(
    FlaskForm, UniqueUserFieldMixin, UniqueEmailFieldMixin, PasswordFieldMixin
):
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Request Password Reset")


class ResetPasswordForm(FlaskForm, PasswordFieldMixin):
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")

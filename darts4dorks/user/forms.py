from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError

from darts4dorks import db
from darts4dorks.models import User


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=32)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=128)])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = db.session.scalar(
                db.select(User).where(User.username == username.data)
            )
            if user is not None:
                raise ValidationError(
                    "That username is taken. Please choose a different one."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = db.session.scalar(db.select(User).where(User.email == email.data))
            if user is not None:
                raise ValidationError("Please use a different email address.")

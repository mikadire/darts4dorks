from flask_wtf import FlaskForm
from wtforms import SubmitField

from darts4dorks.form_utils import UniqueEmailFieldMixin, UniqueUserFieldMixin


class UpdateAccountForm(FlaskForm, UniqueUserFieldMixin, UniqueEmailFieldMixin):
    submit = SubmitField("Update")

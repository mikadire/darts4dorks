from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from darts4dorks import db
from darts4dorks.models import User
from darts4dorks.api.errors import error_response

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = db.session.scalar(db.select(User).where(User.username == username))
    if user and user.verify_password(password):
        return user


@token_auth.verify_token
def verify_token(token):
    return User.check_api_token(token) if token else None


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)

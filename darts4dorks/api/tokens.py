from darts4dorks import db
from darts4dorks.api import bp
from darts4dorks.api.auth import basic_auth, token_auth


@bp.route("/tokens", methods=["POST"])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_api_token()
    db.session.commit()
    return {"token": token}


@bp.route("/tokens", methods=["DELETE"])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_api_token()
    db.session.commit()
    return "", 204

from darts4dorks import db
from darts4dorks.models import Session
from darts4dorks.api import bp
from darts4dorks.stats import get_rtc_stats
from darts4dorks.api.auth import token_auth


@bp.route("/rtc_stats/<int:user_id>", methods=["GET"])
@token_auth.login_required
def rtc_stats(user_id):
    return get_rtc_stats(user_id)

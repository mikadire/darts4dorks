from sqlalchemy import func
from darts4dorks import db
from darts4dorks.models import User, Session, Attempt
from darts4dorks.api import bp
from darts4dorks.api.auth import token_auth


@bp.route("/rtc_stats/<int:user_id>/<int:session_id>", methods=["GET"])
@token_auth.login_required
def rtc_stats(user_id, session_id):
    # check user_id and session_id are valid
    db.get_or_404(User, user_id)
    db.get_or_404(Session, session_id)

    lifetime_stats = db.session.execute(
        db.select(func.avg(Attempt.darts_thrown), func.stddev(Attempt.darts_thrown))
        .join(Session)
        .where(Session.user_id == user_id)
    ).first()
    lifetime_stats = {
        "avg_darts_thrown": lifetime_stats[0],
        "stddev_darts_thrown": lifetime_stats[1],
    }

    session_stats = db.session.execute(
        db.select(
            Attempt.session_id,
            func.avg(Attempt.darts_thrown),
            func.stddev(Attempt.darts_thrown),
        )
        .join(Session)
        .where(Session.user_id == user_id)
        .group_by(Attempt.session_id)
    ).all()
    session_stats = [
        {
            "session_id": row[0],
            "avg_darts_thrown": row[1],
            "stddev_darts_thrown": row[2],
        }
        for row in session_stats
    ]

    session_darts_per_target = db.session.execute(
        (
            db.select(Attempt.target, Attempt.darts_thrown)
            .join(Session)
            .where(Attempt.session_id == session_id, Session.user_id == user_id)
            .order_by(Attempt.target)
        )
    ).all()
    session_darts_per_target = [
        {"target": row[0], "darts_thrown": row[1]} for row in session_darts_per_target
    ]

    lifetime_target_stats = db.session.execute(
        db.select(
            Attempt.target,
            func.avg(Attempt.darts_thrown),
            func.stddev(Attempt.darts_thrown),
        )
        .join(Session)
        .where(Session.user_id == user_id)
        .group_by(Attempt.target)
    ).all()
    lifetime_target_stats = [
        {"target": row[0], "avg_darts_thrown": row[1], "stddev_darts_thrown": row[2]}
        for row in lifetime_target_stats
    ]

    return {
        "lifetime_stats": lifetime_stats,
        "session_stats": session_stats,
        "session_darts_per_target": session_darts_per_target,
        "lifetime_target_stats": lifetime_target_stats,
    }

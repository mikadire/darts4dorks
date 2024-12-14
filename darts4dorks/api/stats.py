from sqlalchemy import func
from darts4dorks.api import bp
from darts4dorks import db
from darts4dorks.models import User, Session, Attempt


@bp.route("/rtc_stats/<int:id>", methods=["GET"])
def rtc_stats(user_id, session_id):
    avg_darts_lifetime = db.session.scalar(db.select(func.avg(Attempt.darts_thrown)))
    avg_darts_per_session = db.session.execute(
        db.select(Attempt.session_id, func.avg(Attempt.darts_thrown)).group_by(
            Attempt.session_id
        )
    ).all()
    darts_thrown_session = db.session.execute(
        (
            db.select(Attempt.target, Attempt.darts_thrown)
            .join(Session)
            .where(Attempt.session_id == session_id, Session.user_id == user_id)
            .order_by(Attempt.target)
        )
    ).all()

    avg_per_target = db.session.execute(
        db.select(
            Attempt.target,
            func.avg(Attempt.darts_thrown),
            func.stddev(Attempt.darts_thrown),
        ).group_by(Attempt.target)
    ).all()

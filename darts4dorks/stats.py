from sqlalchemy import func
from darts4dorks import db
from darts4dorks.models import Session, Attempt


def get_rtc_stats(user_id, session_id):
    lifetime_stats = db.session.execute(
        db.select(func.avg(Attempt.darts_thrown), func.stddev(Attempt.darts_thrown))
        .join(Session)
        .where(Session.user_id == user_id)
    ).first()
    lifetime_stats = {
        "avg_darts_thrown": lifetime_stats[0],
        "stddev_darts_thrown": lifetime_stats[1],
    }

    temporal_session_stats = db.session.execute(
        db.select(
            Attempt.session_id,
            Session.end_time,
            func.avg(Attempt.darts_thrown),
            func.count(Attempt.darts_thrown),
            func.stddev(Attempt.darts_thrown),
        )
        .join(Session)
        .where(Session.user_id == user_id, Session.ended == True)
        .group_by(Attempt.session_id)
    ).all()
    temporal_session_stats = [
        {
            "session_id": row[0],
            "date": row[1],
            "avg_darts_thrown": row[2],
            "total_darts_thrown": row[3],
            "stddev_darts_thrown": row[4],
        }
        for row in temporal_session_stats
    ]

    sessionX_darts_per_target = db.session.execute(
        (
            db.select(Attempt.target, Attempt.darts_thrown)
            .join(Session)
            .where(Attempt.session_id == session_id, Session.user_id == user_id)
            .order_by(Attempt.target)
        )
    ).all()
    sessionX_darts_per_target = [
        {"target": row[0], "darts_thrown": row[1]} for row in sessionX_darts_per_target
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
        "temporal_session_stats": temporal_session_stats,
        "sessionX_darts_per_target": sessionX_darts_per_target,
        "lifetime_target_stats": lifetime_target_stats,
    }

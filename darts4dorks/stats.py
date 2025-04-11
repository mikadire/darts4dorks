from sqlalchemy import func
from darts4dorks import db
from darts4dorks.models import Session, Attempt


def get_rtc_stats(user_id):
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
        .order_by(Session.end_time)
    ).all()

    temporal_session_stats_json = [
        {
            "session_id": row[0],
            "date": row[1],
            "avg_darts_thrown": float(row[2]),
            "total_darts_thrown": row[3],
            "stddev_darts_thrown": row[4],
        }
        for row in temporal_session_stats
    ]

    temporal_target_stats = db.session.execute(
        db.select(Session.id, Session.end_time, Attempt.target, Attempt.darts_thrown)
        .join(Session)
        .where(Session.user_id == user_id, Session.ended == True)
        .order_by(Session.end_time, Attempt.target)
    ).all()

    temporal_target_stats_json = [
        {"session_id": row[0], "date": row[1], "target": row[2], "darts_thrown": row[3]}
        for row in temporal_target_stats
    ]

    lifetime_stats = db.session.execute(
        db.select(func.avg(Attempt.darts_thrown), func.stddev(Attempt.darts_thrown))
        .join(Session)
        .where(Session.user_id == user_id)
    ).one()

    if lifetime_stats[0] is not None:
        lifetime_stats_json = {
            "avg_darts_thrown": float(lifetime_stats[0]),
            "stddev_darts_thrown": lifetime_stats[1],
        }
    else:
        lifetime_stats_json = []

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

    lifetime_target_stats_json = [
        {
            "target": row[0],
            "avg_darts_thrown": float(row[1]),
            "stddev_darts_thrown": row[2],
        }
        for row in lifetime_target_stats
    ]

    return {
        "lifetime_stats": lifetime_stats_json,
        "lifetime_target_stats": lifetime_target_stats_json,
        "temporal_target_stats": temporal_target_stats_json,
        "temporal_session_stats": temporal_session_stats_json,
    }

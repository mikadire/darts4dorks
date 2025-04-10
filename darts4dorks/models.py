import jwt
import secrets
from typing import List
from datetime import datetime, timezone, timedelta
from time import time
from hashlib import md5
from sqlalchemy import String, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, WriteOnlyMapped
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from darts4dorks import db, login_manager


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(128), index=True, unique=True)
    password_hash: Mapped[str | None] = mapped_column(String(256))
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    token: Mapped[str | None] = mapped_column(String(32), index=True, unique=True)
    token_expiration: Mapped[datetime | None]

    sessions: WriteOnlyMapped["Session"] = relationship(back_populates="owner")

    def __repr__(self):
        return (
            f"User(id={self.id}, username={self.username}, "
            f"email={self.email}, created={self.created})"
        )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def create_session(self):
        session = Session(owner=self)
        db.session.add(session)
        return session

    def get_active_session_and_target(self):
        query = (
            db.select(Session, Attempt.target)
            .join_from(Session, Attempt, isouter=True)
            .where(Session.ended == False, Session.owner == self)
            .order_by(Session.id.desc(), Attempt.id.desc())
        )
        return db.session.execute(query).first()

    def get_password_reset_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_password_reset_token(token):
        try:
            id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except:
            return None
        return db.session.get(User, id)

    def get_api_token(self, expires_in=3600):
        now = datetime.now(timezone.utc)
        if self.token and self.token_expiration.replace(
            tzinfo=timezone.utc
        ) > now + timedelta(seconds=60):
            return self.token
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_api_token(self):
        self.token_expiration = datetime.now(timezone.utc) - timedelta(seconds=1)

    @staticmethod
    def check_api_token(token):
        user = db.session.scalar(db.select(User).where(User.token == token))
        if user is None or user.token_expiration.replace(
            tzinfo=timezone.utc
        ) < datetime.now(timezone.utc):
            return None
        return user


class Session(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[datetime] = mapped_column(server_default=func.now())
    end_time: Mapped[datetime | None] = mapped_column(
        onupdate=func.now()
    )  # Initially None, updated to server time when ended is set to True
    ended: Mapped[bool] = mapped_column(default=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)

    owner: Mapped[User] = relationship(back_populates="sessions")
    attempts: Mapped[List["Attempt"]] = relationship(
        back_populates="session",
        cascade="all, delete, delete-orphan",
    )

    def __repr__(self):
        return (
            f"Session(id={self.id}, start={self.start_time}, end={self.end_time}, "
            f"ended={self.ended}, user_id={self.user_id})"
        )


class Attempt(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    target: Mapped[int]
    darts_thrown: Mapped[int]
    session_id: Mapped[int] = mapped_column(
        ForeignKey(Session.id, ondelete="CASCADE"), index=True
    )

    session: Mapped[Session] = relationship(back_populates="attempts")

    __table_args__ = (
        UniqueConstraint("target", "session_id", name="unique_target_per_session"),
    )

    def __repr__(self):
        return (
            f"Attempt(id={self.id}, target={self.target}, "
            f"darts_thrown={self.darts_thrown}, session_id={self.session_id})"
        )


@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))

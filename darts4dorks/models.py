from datetime import datetime
from hashlib import md5
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, WriteOnlyMapped
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from darts4dorks import db, login_manager


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(128), index=True, unique=True)
    password_hash: Mapped[str | None] = mapped_column(String(256))
    created: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)

    sessions: WriteOnlyMapped["Session"] = relationship(back_populates="owner")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def __repr__(self):
        return f"<User {self.id}, {self.username}, {self.created}>"


@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Session(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)
    end_time: Mapped[datetime | None] = mapped_column(
        onupdate=func.now()
    )  # Initially None, updated to server time when ended is set to True
    ended: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)

    owner: Mapped[User] = relationship(back_populates="sessions")
    attempts: WriteOnlyMapped["Attempt"] = relationship(back_populates="session")

    def __repr__(self):
        return f"<ID {self.id}>, <User {self.user_id}>, <Time {self.start_time}>"


class Attempt(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    target: Mapped[int] = mapped_column()  # SB = 21, DB = 22
    darts_thrown: Mapped[int] = mapped_column()
    session_id: Mapped[int] = mapped_column(ForeignKey(Session.id), index=True)

    session: Mapped[Session] = relationship(back_populates="attempts")

    def __repr__(self):
        return f"<{self.id}>, <User {self.user_id}>, <Time {self.start_time}>"

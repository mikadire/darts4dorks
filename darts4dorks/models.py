from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, WriteOnlyMapped
from darts4dorks import db


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(128), index=True, unique=True)
    password: Mapped[str] = mapped_column(String(256))
    # Evaluated server side upon db.session.commit()
    created: Mapped[datetime] = mapped_column(server_default=func.now(), 
                                              index=True)

    sessions: WriteOnlyMapped['Session'] = relationship(back_populates='owner')

    def __repr__(self):
        return f'<User {self.id}, {self.username}, {self.created}>'
    

class Session(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[datetime] = mapped_column(server_default=func.now(), 
                                                 index=True)
    # Initially None, updated to server time when ended is set to True
    end_time:Mapped[datetime | None] = mapped_column(onupdate=func.now())
    ended: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)

    owner: Mapped[User] = relationship(back_populates='sessions')
    attempts: WriteOnlyMapped['Attempt'] = relationship(back_populates='session')

    def __repr__(self):
        return f'<{self.id}>, <User {self.user_id}>, <Time {self.start_time}>'
    

class Attempt(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    # SB = 21, DB = 22
    target: Mapped[int] = mapped_column()
    darts_thrown: Mapped[int] = mapped_column()
    session_id: Mapped[int] = mapped_column(ForeignKey(Session.id), index=True)

    session: Mapped[Session] = relationship(back_populates='attempts')

    def __repr__(self):
        return f'<{self.id}>, <User {self.user_id}>, <Time {self.start_time}>'
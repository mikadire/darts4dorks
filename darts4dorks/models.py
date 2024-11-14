from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, WriteOnlyMapped
from darts4dorks import db


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(128), index=True, unique=True)
    password: Mapped[str] = mapped_column(String(256))
    created: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), index=True
        ) # evaluated server side upon db.session.commit()

    sessions: WriteOnlyMapped['Session'] = relationship(back_populates='owner')

    def __repr__(self):
        return f'<User {self.username}>'
    

class Session(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), index=True
        )
    start_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), index=True
        )
    # Initially None, updated to server time when ended is set to True
    end_time:Mapped[datetime | None] = mapped_column(DateTime, 
                                                     onupdate=func.now())
    ended: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)

    owner: Mapped[User] = relationship(back_populates='sessions')

    def __repr__(self):
        return f'<ID {self.id}>, <User {self.user_id}>'